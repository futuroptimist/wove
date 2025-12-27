function requireEl(id) {
  const el = document.getElementById(id);
  if (!el) {
    console.warn(`viewer: missing DOM element with id ${id}`);
  }
  return el;
}

export function getDom() {
  const statusElement = requireEl('status');
  const roadmapTitleElement = requireEl('roadmap-title');
  const roadmapDescriptionElement = requireEl('roadmap-description');
  const patternStepElement = requireEl('pattern-step');
  const patternStepIndexElement = requireEl('pattern-step-index');
  const patternProgressBarElement = requireEl('pattern-progress-bar');
  const patternPauseToggleElement = requireEl('pattern-pause-toggle');
  const patternPlaybackStatusElement = requireEl('pattern-playback-status');
  const plannerUploadElement = requireEl('planner-upload');
  const plannerUploadLabelElement = requireEl('planner-upload-label');
  const plannerUploadHintElement = requireEl('planner-upload-hint');
  const patternPositionElement = requireEl('pattern-position');
  const patternBoundsElement = requireEl('pattern-bounds');
  const patternDefaultsStatusElement = requireEl('pattern-defaults-status');
  const patternDefaultsListElement = requireEl('pattern-defaults-list');
  const plannerMetadataStatusElement = requireEl('planner-metadata-status');
  const plannerMetadataListElement = requireEl('planner-metadata-details');
  const plannerFileNameElement = requireEl('planner-file-name');
  const plannerFileSizeElement = requireEl('planner-file-size');
  const machineProfileEnvelopeElement = requireEl('machine-profile-envelope');
  const boundsComparisonElement = requireEl('bounds-comparison');
  const machineProfileStatusElement = requireEl('machine-profile-status');
  const machineProfileAxesElement = requireEl('machine-profile-axes');
  const homingGuardStatusElement = requireEl('homing-guard-status');
  const homingGuardHomeStateElement = requireEl('homing-guard-home-state');
  const homingGuardPositionElement = requireEl('homing-guard-position');
  const heatedBedStatusElement = requireEl('heated-bed-status');
  const heatedBedRouteElement = requireEl('heated-bed-route');
  const yarnFlowStatusElement = requireEl('yarn-flow-status');
  const yarnFlowSpoolElement = requireEl('yarn-flow-spool');
  const yarnFlowTotalElement = requireEl('yarn-flow-total');
  const yarnFlowProgressElement = requireEl('yarn-flow-progress');
  const yarnFlowQueueElement = requireEl('yarn-flow-queue');
  const yarnFlowRateElement = requireEl('yarn-flow-rate');
  const yarnFlowUpcomingElement = requireEl('yarn-flow-upcoming');
  const yarnFlowTimingElement = requireEl('yarn-flow-timing');
  const yarnFlowCycleElement = requireEl('yarn-flow-cycle');
  const yarnFlowCalibrationElement = requireEl('yarn-flow-calibration');
  const yarnFlowTensionElement = requireEl('yarn-flow-tension');
  const yarnFlowPositionElement = requireEl('yarn-flow-position');

  return {
    statusElement,
    roadmapTitleElement,
    roadmapDescriptionElement,
    patternStepElement,
    patternStepIndexElement,
    patternProgressBarElement,
    patternPauseToggleElement,
    patternPlaybackStatusElement,
    plannerUploadElement,
    plannerUploadLabelElement,
    plannerUploadHintElement,
    patternPositionElement,
    patternBoundsElement,
    patternDefaultsStatusElement,
    patternDefaultsListElement,
    plannerMetadataStatusElement,
    plannerMetadataListElement,
    plannerFileNameElement,
    plannerFileSizeElement,
    machineProfileEnvelopeElement,
    boundsComparisonElement,
    machineProfileStatusElement,
    machineProfileAxesElement,
    homingGuardStatusElement,
    homingGuardHomeStateElement,
    homingGuardPositionElement,
    heatedBedStatusElement,
    heatedBedRouteElement,
    yarnFlowStatusElement,
    yarnFlowSpoolElement,
    yarnFlowTotalElement,
    yarnFlowProgressElement,
    yarnFlowQueueElement,
    yarnFlowRateElement,
    yarnFlowUpcomingElement,
    yarnFlowTimingElement,
    yarnFlowCycleElement,
    yarnFlowCalibrationElement,
    yarnFlowTensionElement,
    yarnFlowPositionElement,
  };
}
