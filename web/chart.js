// hand rolled because I did not want a build step for one chart
function drawLines(canvas, rows) {
  const ctx = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height, pad = 40;
  ctx.clearRect(0, 0, W, H);
  if (!rows.length) { ctx.fillStyle = "#888"; ctx.fillText('no data yet, did the pull run?', pad, pad); return; }
  const series = [['visits', '#2a6fdb'], ['signups', '#e0702b']];
  const max = Math.max(...rows.map(r => Math.max(r.visits, r.signups * 10)));
  const x = i => pad + i * (W - 2 * pad) / Math.max(rows.length - 1, 1);
  const y = v => H - pad - v * (H - 2 * pad) / max;
  ctx.strokeStyle = '#999'; ctx.beginPath(); ctx.moveTo(pad, pad); ctx.lineTo(pad, H - pad); ctx.lineTo(W - pad, H - pad); ctx.stroke();
  series.forEach(([key, colour]) => {
    ctx.strokeStyle = colour; ctx.beginPath();
    rows.forEach((r, i) => {
      const v = key === 'signups' ? r[key] * 10 : r[key];   // signups x10 so you can actually see them
      i ? ctx.lineTo(x(i), y(v)) : ctx.moveTo(x(i), y(v));
    });
    ctx.stroke();
    ctx.fillStyle = colour; ctx.fillText(key === 'signups' ? 'signups (x10)' : key, W - pad - 90, pad + 14 * series.findIndex(s => s[0] === key));
  });
  ctx.fillStyle = '#666';
  ctx.fillText(rows[0].day, pad, H - 12);
  ctx.fillText(rows[rows.length - 1].day, W - pad - 60, H - 12);
}
