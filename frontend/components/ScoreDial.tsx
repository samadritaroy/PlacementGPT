"use client";

import { useEffect, useState } from "react";

interface Props {
  value: number;
  size?: number;
}

function colorFor(v: number) {
  if (v >= 7) return "#5FA777";
  if (v >= 5) return "#D9A441";
  return "#C1554B";
}

export default function ScoreDial({ value, size = 100 }: Props) {
  const [animated, setAnimated] = useState(0);

  useEffect(() => {
    const t = setTimeout(() => setAnimated(value), 60);
    return () => clearTimeout(t);
  }, [value]);

  const r = size / 2 - 12;
  const center = size / 2;
  const startAngle = -210;
  const sweep = 240;
  const pct = Math.min(1, Math.max(0, animated / 10));
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

  const ticks = Array.from({ length: 11 }, (_, i) => i);
  const color = colorFor(animated);

  return (
    <svg width={size} height={size}>
      {ticks.map((t) => {
        const angle = startAngle + (sweep * t) / 10;
        const inner = polar(angle, r - 5);
        const outer = polar(angle, r + 2);
        const major = t % 5 === 0;
        return (
          <line key={t} x1={inner.x} y1={inner.y} x2={outer.x} y2={outer.y}
            stroke={major ? "#8B92A3" : "#252B38"} strokeWidth={major ? 1.5 : 1} />
        );
      })}
      <path d={arcPath(startAngle, startAngle + sweep, r)} fill="none" stroke="#1A1F2A" strokeWidth={7} strokeLinecap="round" />
      <path
        d={arcPath(startAngle, valueAngle, r)} fill="none" stroke={color} strokeWidth={7} strokeLinecap="round"
        style={{ transition: "all 0.7s cubic-bezier(.4,0,.2,1)" }}
      />
      <text x={center} y={center + size * 0.07} textAnchor="middle" className="font-mono"
        fontSize={size * 0.22} fontWeight={700} fill="#ECE8DE">
        {animated.toFixed(1)}
      </text>
    </svg>
  );
}