import type {ComponentType} from "react";
import type {TemplateProps} from "./templates/NineTemplates";
import {KeywordTemplate, CalloutTemplate, OpinionCardsTemplate, DataChartTemplate, LogicFlowTemplate, ComparisonTemplate, TimelineTemplate, EvidenceTemplate, BrandMapTemplate} from "./templates/NineTemplates";
import {ExampleClip} from "./clips/ExampleClip";

export const clipRegistry: Record<string, ComponentType<TemplateProps>> = {
  ExampleClip,
  KeywordTemplate,
  CalloutTemplate,
  OpinionCardsTemplate,
  DataChartTemplate,
  LogicFlowTemplate,
  ComparisonTemplate,
  TimelineTemplate,
  EvidenceTemplate,
  BrandMapTemplate,

};
