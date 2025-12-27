const elementIds = {
  statusElement: 'status',
  roadmapTitleElement: 'roadmap-title',
  roadmapDescriptionElement: 'roadmap-description',
  patternStepElement: 'pattern-step',
  patternStepIndexElement: 'pattern-step-index',
  patternProgressBarElement: 'pattern-progress-bar',
  patternPauseToggleElement: 'pattern-pause-toggle',
  patternPlaybackStatusElement: 'pattern-playback-status',
  plannerUploadElement: 'planner-upload',
  plannerUploadLabelElement: 'planner-upload-label',
  plannerUploadHintElement: 'planner-upload-hint',
  patternPositionElement: 'pattern-position',
  patternBoundsElement: 'pattern-bounds',
  patternDefaultsStatusElement: 'pattern-defaults-status',
  patternDefaultsListElement: 'pattern-defaults-list',
  plannerMetadataStatusElement: 'planner-metadata-status',
  plannerMetadataListElement: 'planner-metadata-details',
  machineProfileEnvelopeElement: 'machine-profile-envelope',
  boundsComparisonElement: 'bounds-comparison',
  machineProfileStatusElement: 'machine-profile-status',
  machineProfileAxesElement: 'machine-profile-axes',
  homingGuardStatusElement: 'homing-guard-status',
  homingGuardHomeStateElement: 'homing-guard-home-state',
  homingGuardPositionElement: 'homing-guard-position',
  heatedBedStatusElement: 'heated-bed-status',
  heatedBedRouteElement: 'heated-bed-route',
  yarnFlowStatusElement: 'yarn-flow-status',
  yarnFlowSpoolElement: 'yarn-flow-spool',
  yarnFlowTotalElement: 'yarn-flow-total',
  yarnFlowProgressElement: 'yarn-flow-progress',
  yarnFlowQueueElement: 'yarn-flow-queue',
  yarnFlowRateElement: 'yarn-flow-rate',
  yarnFlowUpcomingElement: 'yarn-flow-upcoming',
  yarnFlowTimingElement: 'yarn-flow-timing',
  yarnFlowCycleElement: 'yarn-flow-cycle',
  yarnFlowCalibrationElement: 'yarn-flow-calibration',
  yarnFlowTensionElement: 'yarn-flow-tension',
  yarnFlowPositionElement: 'yarn-flow-position',
};

export function getUiElements(root = document) {
  return Object.fromEntries(
    Object.entries(elementIds).map(([key, id]) => [key, root.getElementById(id)]),
  );
}

export function warnIfMissingElements(elements) {
  Object.entries(elements).forEach(([key, element]) => {
    if (!element) {
      console.warn(`Missing UI element: ${key}`);
    }
  });
}

export function getUiElementIds() {
  return { ...elementIds };
}
