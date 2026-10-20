import {Easing, interpolate, useCurrentFrame, useVideoConfig} from "remotion";
import {C, clamp, Header, Page} from "../components";

const Bottle = ({small = false}: {small?: boolean}) => (
  <svg viewBox="0 0 160 245" width="100%" height="100%" aria-label={small ? "小样" : "正装"}>
    <rect x="47" y="3" width="66" height="45" rx="8" fill={C.ink}/>
    <rect x="23" y="43" width="114" height="197" rx="22" fill={small ? C.accent : C.paper} stroke={C.ink} strokeWidth="3"/>
    <path d="M37 67 V205" stroke="white" strokeWidth="7" strokeLinecap="round" opacity=".45"/>
    <rect x="32" y="115" width="96" height="60" rx="6" fill={small ? C.paper : C.ink}/>
    <text x="80" y="155" textAnchor="middle" fontSize="30" fontWeight="700" fill={small ? C.ink : C.paper}>{small ? "小样" : "正装"}</text>
  </svg>
);

// Frame marks mirror motionDesign. Seconds remain correct if the fps changes.
export const ExampleClip = () => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const landscape = width >= height;
  const t = frame / fps;
  const reveal = (start: number) => interpolate(t, [start, start + .5], [0, 1], clamp);
  const move = interpolate(t, [2, 95 / 30], [0, 1], {...clamp, easing: Easing.bezier(.4, 0, .2, 1)});
  const old = interpolate(t, [2, 95 / 30], [1, 0], clamp);
  return (
    <Page>
      <Header start={-22}>小样的角色变了</Header>
      <div style={{position: "absolute", left: 100, right: 100, top: landscape ? 225 : 435, textAlign: "center", fontSize: 50, fontWeight: 700}}>
        <div style={{opacity: old}}>买正装，送小样</div>
        <div style={{position: "absolute", inset: 0, opacity: reveal(95 / 30)}}>从附赠到单独售卖</div>
      </div>
      <div style={{position: "absolute", left: landscape ? 520 : 240, top: landscape ? 350 : 695, width: landscape ? 220 : 300, height: landscape ? 337 : 459, opacity: old}}><Bottle/></div>
      <div style={{position: "absolute", left: landscape ? 990 : 625, top: landscape ? 740 : 1245, fontSize: 40, opacity: old}}>附赠</div>
      <div style={{position: "absolute", left: landscape ? 990 - 70 * move : 650 - 190 * move, top: landscape ? 440 + 70 * move : 910 - 5 * move, width: 160, height: 245, transformOrigin: "50% 100%", scale: 1 + .6 * move}}><Bottle small/></div>
      <div style={{position: "absolute", left: landscape ? 600 : 180, top: landscape ? 757 : 1158, width: 720, height: 18, background: C.ink, borderRadius: 9, opacity: reveal(4)}}/>
      <div style={{position: "absolute", left: landscape ? 600 : 180, top: landscape ? 776 : 1177, width: 720, height: 60, background: C.paper, borderBottom: `3px solid ${C.line}`, opacity: reveal(4)}}/>
      <div style={{position: "absolute", left: landscape ? 600 : 180, top: landscape ? 850 : 1280, width: 720, textAlign: "center", fontSize: 42, opacity: reveal(4)}}>自己的货架</div>
      <div style={{position: "absolute", left: landscape ? 1180 : 706, top: landscape ? 400 : 855, padding: "20px 22px", border: `3px solid ${C.accent}`, borderRadius: 12, background: C.paper, fontSize: 38, lineHeight: 1.25, fontWeight: 700, rotate: "5deg", opacity: reveal(5.5)}}>自己的<br/>价格</div>
      <div style={{position: "absolute", left: landscape ? 440 : 385, top: landscape ? 400 : 640, width: 310, textAlign: "center", padding: "20px 0", borderRadius: 50, background: C.accentSecondary, fontSize: 42, fontWeight: 700, opacity: reveal(7)}}>自己的活动</div>
      <div style={{position: "absolute", left: landscape ? 1350 : 120, right: 120, top: landscape ? 550 : 1530, textAlign: "center", fontSize: 44, lineHeight: 1.35, opacity: reveal(7.5)}}>同一个小样<br/><strong>有了独立的经营身份</strong></div>
    </Page>
  );
};
