export function normalizeAxisBounds(bounds) {
  if (!bounds || typeof bounds !== 'object') {
    return null;
  }
  const min = Number(bounds.min ?? bounds.min_mm ?? bounds.minimum ?? bounds.low);
  const max = Number(bounds.max ?? bounds.max_mm ?? bounds.maximum ?? bounds.high);
  if (!Number.isFinite(min) || !Number.isFinite(max) || max < min) {
    return null;
  }
  return { min, max };
}

export function comparePlannerToMachineBounds(plannerBounds, machineBounds) {
  const axes = ['x', 'y', 'z'];
  const normalizedPlanner = {};
  const normalizedMachine = {};
  const missingPlannerAxes = [];
  const missingMachineAxes = [];
  axes.forEach((axis) => {
    normalizedPlanner[axis] = normalizeAxisBounds(plannerBounds?.[axis]);
    normalizedMachine[axis] = normalizeAxisBounds(machineBounds?.[axis]);
    if (!normalizedPlanner[axis]) {
      missingPlannerAxes.push(axis);
    }
    if (!normalizedMachine[axis]) {
      missingMachineAxes.push(axis);
    }
  });

  const missingPlanner = missingPlannerAxes.length > 0;
  const missingMachine = missingMachineAxes.length > 0;
  const details = {};
  const exceedingAxes = [];

  axes.forEach((axis) => {
    const planner = normalizedPlanner[axis];
    const machine = normalizedMachine[axis];
    if (!planner || !machine) {
      return;
    }
    const overrunLow = planner.min < machine.min;
    const overrunHigh = planner.max > machine.max;
    if (overrunLow || overrunHigh) {
      exceedingAxes.push(axis);
    }
    details[axis] = {
      planner,
      machine,
      overrunLow,
      overrunHigh,
    };
  });

  const fits = !missingPlanner && !missingMachine && exceedingAxes.length === 0;

  return {
    missingPlanner,
    missingMachine,
    missingPlannerAxes,
    missingMachineAxes,
    fits,
    exceedingAxes,
    details,
  };
}
