# Repository maintenance

## Common Failure Patterns

| Symptom | Root cause | Fix |
|---|---|---|
| Two repositories could publish the same distribution | Duplicate release workflows for one namespace | Designate canonical source, disable legacy publisher, preserve historical code |
