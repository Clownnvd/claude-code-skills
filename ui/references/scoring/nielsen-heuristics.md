# Nielsen's 10 Heuristics — Quick Audit Checklist

Cross-check after scoring. Each heuristic is pass/fail with severity 0-4.

**Severity scale**: 0=Not a problem, 1=Cosmetic, 2=Minor, 3=Major, 4=Catastrophe

## H1: Visibility of System Status
- [ ] Loading indicators for async operations
- [ ] Progress bars for multi-step flows
- [ ] Active state on current nav item
- [ ] Form submission feedback (success/error)
- [ ] Real-time validation as user types

## H2: Match Between System and Real World
- [ ] Familiar terminology (no internal jargon)
- [ ] Icons match user expectations
- [ ] Logical ordering (dates chronological, prices low→high)
- [ ] Metaphors make sense (trash can = delete)

## H3: User Control and Freedom
- [ ] Undo/redo available for destructive actions
- [ ] Easy navigation back (breadcrumbs, back button)
- [ ] Escape closes modals and overlays
- [ ] Cancel option on all forms
- [ ] Clear way to reset filters/search

## H4: Consistency and Standards
- [ ] Same action = same visual treatment everywhere
- [ ] Button styles consistent (primary, secondary, ghost)
- [ ] Icon usage consistent (same icon = same meaning)
- [ ] Spacing consistent between similar elements
- [ ] Platform conventions followed (link = blue/underline)

## H5: Error Prevention
- [ ] Confirmation for destructive actions (delete, payment)
- [ ] Input constraints prevent invalid data (date picker vs text)
- [ ] Disabling submit until form valid
- [ ] Autosave for long forms
- [ ] Type-ahead suggestions for common inputs

## H6: Recognition Rather Than Recall
- [ ] Labels visible at all times (not just placeholders)
- [ ] Recent/frequent items suggested
- [ ] Instructions visible where needed (not in separate page)
- [ ] Search with suggestions and filters
- [ ] Context preserved when navigating back

## H7: Flexibility and Efficiency of Use
- [ ] Keyboard shortcuts for power users
- [ ] Default values for common inputs
- [ ] Bulk actions for repetitive tasks
- [ ] Customizable dashboard/views
- [ ] Quick actions accessible (right-click, swipe)

## H8: Aesthetic and Minimalist Design
- [ ] No unnecessary decorative elements
- [ ] Every element serves a purpose
- [ ] Visual noise minimized
- [ ] Whitespace used effectively
- [ ] Information density appropriate for audience

## H9: Help Users Recognize, Diagnose, Recover from Errors
- [ ] Error messages in plain language (not codes)
- [ ] Error identifies the problem specifically
- [ ] Error suggests how to fix it
- [ ] Error message near the source (not just top-of-page toast)
- [ ] Form doesn't clear valid fields on error

## H10: Help and Documentation
- [ ] Tooltips for non-obvious features
- [ ] Onboarding for first-time users
- [ ] Help accessible from every page
- [ ] FAQ for common questions
- [ ] Contact/support option visible

## Using This Checklist
1. Go through each heuristic
2. Check each item — mark failures
3. Rate severity (0-4) for each failure
4. Prioritize fixes: severity 4 first, then 3, then 2
5. Report alongside the main scorecard
