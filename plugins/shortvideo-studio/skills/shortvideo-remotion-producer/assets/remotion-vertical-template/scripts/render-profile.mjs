export const profileFor = (clip) => clip.renderProfile ?? "h264";
export const renderArgs = (clip, preview = false) => {
  const profile = preview ? "h264" : profileFor(clip);
  if (profile === "prores-alpha") return ["--codec=prores", "--prores-profile=4444", "--pixel-format=yuva444p10le", "--image-format=png"];
  if (profile === "vp9-alpha") return ["--codec=vp9", "--pixel-format=yuva420p", "--image-format=png", "--crf=18"];
  return ["--codec=h264", "--pixel-format=yuv420p", `--crf=${preview ? 28 : 18}`];
};
export const previewName = (clip) => clip.fileName.replace(/\.(mov|webm)$/, ".mp4");
