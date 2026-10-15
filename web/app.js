"use strict";

// pwdgen web — offline password & passphrase generator.
// All randomness comes from the Web Crypto API (crypto.getRandomValues).

const LOWERCASE = "abcdefghijklmnopqrstuvwxyz";
const UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
const DIGITS = "0123456789";
const SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?";
const AMBIGUOUS = "Il1O0o";

/** Uniform random integer in [0, max) using rejection sampling. */
function randomInt(max) {
  const limit = Math.floor(0xffffffff / max) * max;
  const buf = new Uint32Array(1);
  let x;
  do {
    crypto.getRandomValues(buf);
    x = buf[0];
  } while (x >= limit);
  return x % max;
}

function choice(seq) {
  return seq[randomInt(seq.length)];
}

function buildCharset({ lower, upper, digits, symbols, excludeAmbiguous }) {
  let pool = "";
  if (lower) pool += LOWERCASE;
  if (upper) pool += UPPERCASE;
  if (digits) pool += DIGITS;
  if (symbols) pool += SYMBOLS;
  if (!pool) throw new Error("Select at least one character type.");
  if (excludeAmbiguous) {
    pool = [...pool].filter((ch) => !AMBIGUOUS.includes(ch)).join("");
  }
  return pool;
}

function generatePassword(length, charset) {
  let out = "";
  for (let i = 0; i < length; i += 1) out += choice(charset);
  return out;
}

function generatePassphrase({ words, separator, capitalize, includeNumber }) {
  const chosen = [];
  for (let i = 0; i < words; i += 1) {
    const w = choice(window.BIP39_WORDS);
    chosen.push(capitalize ? w[0].toUpperCase() + w.slice(1) : w);
  }
  if (includeNumber) {
    chosen.splice(randomInt(chosen.length + 1), 0, String(randomInt(10)));
  }
  return chosen.join(separator);
}

function entropyBits(length, poolSize, isPassphrase, words, includeNumber) {
  if (isPassphrase) {
    let bits = words * Math.log2(2048);
    if (includeNumber) bits += Math.log2(10) + Math.log2(words + 1);
    return bits;
  }
  return length * Math.log2(poolSize);
}

function strengthLabel(bits) {
  if (bits < 28) return "Very weak";
  if (bits < 36) return "Weak";
  if (bits < 60) return "Reasonable";
  if (bits < 128) return "Strong";
  return "Very strong";
}

function strengthPercent(bits) {
  return Math.max(4, Math.min(100, Math.round((bits / 128) * 100)));
}

// ---- UI wiring ----

const el = (id) => document.getElementById(id);
let currentMode = "password";

function render() {
  const output = el("output");
  const meta = el("meta");

  try {
    let value;
    let bits;
    if (currentMode === "passphrase") {
      const words = Number(el("words").value);
      const separator = el("separator").value || "-";
      value = generatePassphrase({
        words,
        separator,
        capitalize: el("capitalize").checked,
        includeNumber: el("number").checked,
      });
      bits = entropyBits(0, 0, true, words, el("number").checked);
    } else {
      const charset = buildCharset({
        lower: !el("noLower").checked,
        upper: !el("noUpper").checked,
        digits: !el("noDigits").checked,
        symbols: el("symbols").checked,
        excludeAmbiguous: el("ambiguous").checked,
      });
      const length = Number(el("length").value);
      value = generatePassword(length, charset);
      bits = entropyBits(length, new Set(charset).size, false, 0, false);
    }

    output.textContent = value;
    const percent = strengthPercent(bits);
    meta.innerHTML =
      '<div class="bar"><span style="width:' +
      percent +
      '%"></span></div>' +
      "<small>" +
      strengthLabel(bits) +
      " · ~" +
      bits.toFixed(0) +
      " bits of entropy</small>";
  } catch (err) {
    output.textContent = "";
    meta.innerHTML = '<small class="error">' + err.message + "</small>";
  }
}

function setMode(mode) {
  currentMode = mode;
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.classList.toggle("active", tab.dataset.mode === mode);
  });
  el("password-panel").hidden = mode !== "password";
  el("passphrase-panel").hidden = mode !== "passphrase";
  render();
}

async function copyOutput() {
  const text = el("output").textContent;
  if (!text) return;
  try {
    await navigator.clipboard.writeText(text);
  } catch {
    const range = document.createRange();
    range.selectNodeContents(el("output"));
    const sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
    document.execCommand("copy");
  }
  const btn = el("copy");
  const original = btn.textContent;
  btn.textContent = "Copied!";
  setTimeout(() => {
    btn.textContent = original;
  }, 1200);
}

document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".tab").forEach((tab) => {
    tab.addEventListener("click", () => setMode(tab.dataset.mode));
  });
  document.querySelectorAll("input").forEach((input) => {
    input.addEventListener("input", render);
    input.addEventListener("change", render);
  });
  el("copy").addEventListener("click", copyOutput);
  el("regenerate").addEventListener("click", render);
  setMode("password");
});
