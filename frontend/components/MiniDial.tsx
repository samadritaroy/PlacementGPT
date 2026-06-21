interface MiniDialProps {
  value: number; // 0–10
  size?: number;
}

function colorFor(v: number) {
  if (v >= 7) return "#5FA777";
  if (v >= 5) return "#D9A441";
  return "#C1554B";
}

// Static, server-renderable — no hooks, no client JS needed.
export default function MiniDial({ value, size = 100 }: MiniDialProps) {
  const r = size / 2 - 10;
  const center = size / 2;
  const startAngle = -210;
  const sweep = 240;
  const pct = Math.min(1, Math.max(0, value / 10));
  const valueAngle = startAngle + sweep * pct;

  const polar = (angleDeg: number, radius: number) => {
    const rad = (angleDeg * Math.PI) / 180;
    return { x: center + radius * Math.cos(rad), y: center + radius * Math.sin(rad) };
  };

  const arcPath = (a0: number, a1: number, radius: number) => {
    const p0 = polar(a0, radius);
    const p1 = polar(a1, radius);
    const largeArc = a1 - a0 > 180 ? 1 : 0;
    return `M ${p0.x} ${p0.y} A ${radius} ${radius} 0 ${largeArc} 1 ${p1.x} ${p1.y}`;
  };

  const color = colorFor(value);

  return (
    <svg width={size} height={size}>
      <path
        d={arcPath(startAngle, startAngle + sweep, r)}
        fill="none" stroke="#1A1F2A" strokeWidth={7} strokeLinecap="round"
      />
      <path
        d={arcPath(startAngle, valueAngle, r)}
        fill="none" stroke={color} strokeWidth={7} strokeLinecap="round"
      />
      <text
        x={center} y={center + size * 0.07} textAnchor="middle"
        fontFamily="ui-monospace, SFMono-Regular, Menlo, monospace"
        fontSize={size * 0.26} fontWeight={700} fill="#ECE8DE"
      >
        {value.toFixed(1)}
      </text>
    </svg>
  );
}