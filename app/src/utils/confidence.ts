export const getConfidenceColorClass = (score?: number): string => {
  if (score === undefined) return "confidence-low";
  if (score >= 0.9) return "confidence-high";
  if (score >= 0.5) return "confidence-med";
  return "confidence-low";
};
