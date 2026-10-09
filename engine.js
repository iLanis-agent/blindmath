// Blind math engine - window blind sizing arithmetic.
// Pure functions, no DOM. All borrowed norms are labeled in the UI, not buried here.
'use strict';

function round1(x) { return Math.round(x * 10) / 10; }

// --- Inside-mount order size -------------------------------------------------
// Measure the opening in three places. Order width comes from the SMALLEST
// width minus the maker's clearance deduction; order drop comes from the
// LONGEST drop so the blind reaches the sill everywhere.
function insideMount(wTop, wMid, wBot, dLeft, dMid, dRight, deduction) {
  var widths = [wTop, wMid, wBot], drops = [dLeft, dMid, dRight], i;
  for (i = 0; i < 3; i++) {
    if (!(widths[i] > 0)) return { error: 'widths must be positive' };
    if (!(drops[i] > 0)) return { error: 'drops must be positive' };
  }
  if (!(deduction >= 0)) return { error: 'deduction must not be negative' };
  var wMin = Math.min(wTop, wMid, wBot);
  var wMax = Math.max(wTop, wMid, wBot);
  var dMax = Math.max(dLeft, dMid, dRight);
  var orderWidth = round1(wMin - deduction);
  if (!(orderWidth > 0)) return { error: 'deduction leaves no width' };
  var bow = round1(wMax - wMin);
  var square = bow <= 1
    ? 'square opening'
    : 'out of square by ' + bow + ' cm - expect small light gaps at the wide end';
  return { orderWidth: orderWidth, orderDrop: round1(dMax), bow: bow, square: square };
}

// --- Venetian slat count -----------------------------------------------------
// Pitch is slat width minus overlap; slats cover n*slatW - (n-1)*overlap.
function slats(drop, slatW, overlap) {
  if (!(drop > 0)) return { error: 'drop must be positive' };
  if (!(slatW > 0)) return { error: 'slat width must be positive' };
  if (!(overlap >= 0)) return { error: 'overlap must not be negative' };
  if (overlap >= slatW) return { error: 'overlap must be less than slat width' };
  var pitch = slatW - overlap;
  var n = Math.ceil(drop / pitch);
  var coverage = round1(n * slatW - (n - 1) * overlap);
  return { count: n, pitch: round1(pitch), coverage: coverage };
}

// --- Split a wide span -------------------------------------------------------
// Wide windows take several blinds side by side; split the span evenly.
function splitSpan(span, maxWidth) {
  if (!(span > 0)) return { error: 'span must be positive' };
  if (!(maxWidth > 0)) return { error: 'max width must be positive' };
  var n = Math.ceil(span / maxWidth);
  var each = round1(span / n);
  var verdict = n === 1 ? 'one blind does it'
    : each < 40 ? n + ' narrow blinds - a valance helps the joins'
    : n + ' blinds, even split';
  return { count: n, each: each, verdict: verdict };
}

// --- Text rendering (shared by UI and tests) ---------------------------------
function renderInside(r) {
  if (r.error) return r.error;
  return 'Order ' + r.orderWidth + ' cm wide x ' + r.orderDrop + ' cm drop. ' + r.square + '.';
}
function renderSlats(r) {
  if (r.error) return r.error;
  return r.count + ' slats at ' + r.pitch + ' cm pitch cover ' + r.coverage + ' cm.';
}
function renderSplit(r) {
  if (r.error) return r.error;
  if (r.count === 1) return r.verdict + ' at ' + r.each + ' cm.';
  return r.count + ' blinds of ' + r.each + ' cm each - ' + r.verdict + '.';
}

var api = {
  round1: round1,
  insideMount: insideMount,
  slats: slats,
  splitSpan: splitSpan,
  renderInside: renderInside,
  renderSlats: renderSlats,
  renderSplit: renderSplit
};
if (typeof module !== 'undefined' && module.exports) module.exports = api;
if (typeof window !== 'undefined') window.BlindMath = api;
