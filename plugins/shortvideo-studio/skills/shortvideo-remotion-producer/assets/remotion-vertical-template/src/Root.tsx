import {Composition} from "remotion";
import manifest from "../project-manifest.json";
import type {TemplateProps} from "./templates/NineTemplates";
import {clipRegistry} from "./clip-registry";

export const RemotionRoot: React.FC = () => (
  <>
    {manifest.clips.map((clip) => {
      const component = clipRegistry[clip.compositionId];
      if (!component) {
        throw new Error(`Missing clip registry entry for ${clip.compositionId}`);
      }

      return (
        <Composition
          key={clip.compositionId}
          id={clip.compositionId}
          component={component}
          defaultProps={{...((clip as {templateProps?: TemplateProps}).templateProps ?? {}), presentation: (clip as {presentation?: "fullscreen" | "overlay"}).presentation ?? "fullscreen"}}
          durationInFrames={clip.durationInFrames}
          fps={manifest.video.fps}
          width={manifest.video.width}
          height={manifest.video.height}
        />
      );
    })}
  </>
);
