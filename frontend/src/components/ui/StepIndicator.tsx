interface Props {
  steps: string[];
  current: number;
  onSelect?: (index: number) => void;
}

export function StepIndicator({ steps, current, onSelect }: Props) {
  return (
    <ol className="step-indicator">
      {steps.map((label, index) => {
        const state = index === current ? "active" : index < current ? "done" : "todo";
        return (
          <li
            key={label}
            className={`step-indicator-item step-indicator-${state}`}
            onClick={() => onSelect?.(index)}
          >
            <span className="step-indicator-number">{index < current ? "✓" : index + 1}</span>
            <span className="step-indicator-label">{label}</span>
          </li>
        );
      })}
    </ol>
  );
}
