import type {CSSProperties, ReactNode} from "react";
import {AbsoluteFill, Easing, Interactive, interpolate, useCurrentFrame, useVideoConfig} from "remotion";
import manifest from "../project-manifest.json";

export const C = manifest.styleTokens;

export const clamp = {
  extrapolateLeft: "clamp" as const,
  extrapolateRight: "clamp" as const,
};

export const Page = ({children, border = false}: {children: ReactNode; index?: string; border?: boolean}) => (
  <AbsoluteFill
    style={{
      backgroundColor: C.background,
      color: C.ink,
      overflow: "hidden",
    }}
  >
    {children}
    {border && <div
      style={{
        position: "absolute",
        inset: 24,
        border: `2px solid ${C.line}`,
        pointerEvents: "none",
        opacity: 0.36,
        zIndex: 300,
      }}
    />}
  </AbsoluteFill>
);

export const Header = ({children, start = 0}: {children: ReactNode; start?: number}) => {
  const frame = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const landscape = width >= height;
  return (
    <Interactive.Div
      name="主标题"
      style={{
        position: "absolute",
        left: landscape ? 96 : 72,
        right: landscape ? 96 : 72,
        top: landscape ? 72 : 120,
        minHeight: landscape ? 96 : 190,
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        textAlign: "center",
        fontSize: landscape ? 72 : 78,
        lineHeight: 1.12,
        fontWeight: 950,
        letterSpacing: -2.5,
        wordBreak: "keep-all",
        zIndex: 160,
        opacity: interpolate(frame, [start, start + 12], [0, 1], clamp),
        translate: `0px ${interpolate(frame, [start, start + 22], [42, 0], {
          ...clamp,
          easing: Easing.bezier(0.16, 1, 0.3, 1),
        })}px`,
      }}
    >
      {children}
    </Interactive.Div>
  );
};

export const Card = ({children, style}: {children: ReactNode; style?: CSSProperties}) => (
  <div
    style={{
      background: C.paper,
      border: `2px solid ${C.line}`,
      borderRadius: 22,
      boxShadow: `0 18px 42px ${C.shadow}`,
      overflow: "hidden",
      ...style,
    }}
  >
    {children}
  </div>
);

export const Takeaway = ({children, start}: {children: ReactNode; start: number}) => {
  const frame = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const landscape = width >= height;
  return (
    <Interactive.Div
      name="底部结论"
      style={{
        position: "absolute",
        left: landscape ? 96 : 72,
        right: landscape ? 96 : 72,
        bottom: landscape ? 120 : 240,
        minHeight: landscape ? 96 : 150,
        padding: "26px 38px",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        textAlign: "center",
        borderRadius: 16,
        background: C.ink,
        color: C.paper,
        boxShadow: `0 20px 44px ${C.shadow}`,
        fontSize: landscape ? 42 : 48,
        lineHeight: 1.16,
        fontWeight: 900,
        wordBreak: "keep-all",
        zIndex: 200,
        opacity: interpolate(frame, [start, start + 12], [0, 1], clamp),
        translate: `0px ${interpolate(frame, [start, start + 22], [100, 0], {
          ...clamp,
          easing: Easing.spring({damping: 18}),
        })}px`,
      }}
    >
      {children}
    </Interactive.Div>
  );
};
