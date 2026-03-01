# CViet Editor-Specific Patterns

## 8.1 Multi-Step CV Editor Store

Based on the CViet `EditorStep` type and `CVData` structure:

```typescript
// src/stores/cv-editor-store.ts
import { create } from 'zustand'
import { devtools, subscribeWithSelector } from 'zustand/middleware'
import { immer } from 'zustand/middleware/immer'
import type {
  CVData,
  EditorStep,
  PersonalInfo,
  Experience,
  Education,
  SkillGroup,
  Language,
  Certification,
} from '@/types/cv'

interface CVEditorState {
  // ---- Data ----
  cvId: string | null
  cvData: CVData
  originalData: CVData | null  // For dirty checking

  // ---- Navigation ----
  currentStep: EditorStep
  completedSteps: Set<EditorStep>

  // ---- UI State ----
  isDirty: boolean
  isSaving: boolean
  lastSavedAt: Date | null
  aiPanelOpen: boolean

  // ---- Actions: Navigation ----
  setStep: (step: EditorStep) => void
  markStepCompleted: (step: EditorStep) => void
  nextStep: () => void
  prevStep: () => void

  // ---- Actions: Data ----
  initFromServer: (cvId: string, data: CVData) => void
  updatePersonalInfo: (info: Partial<PersonalInfo>) => void
  addExperience: (exp: Experience) => void
  updateExperience: (id: string, patch: Partial<Experience>) => void
  removeExperience: (id: string) => void
  reorderExperience: (fromIndex: number, toIndex: number) => void
  addEducation: (edu: Education) => void
  updateEducation: (id: string, patch: Partial<Education>) => void
  removeEducation: (id: string) => void
  updateSkillGroups: (groups: SkillGroup[]) => void
  updateLanguages: (langs: Language[]) => void
  updateCertifications: (certs: Certification[]) => void
  applyAIPatch: (patch: Partial<CVData>) => void

  // ---- Actions: Saving ----
  setSaving: (saving: boolean) => void
  markSaved: () => void
  reset: () => void
}

const STEP_ORDER: EditorStep[] = [
  'personal', 'experience', 'education', 'skills', 'languages', 'certifications'
]

const EMPTY_CV_DATA: CVData = {
  personalInfo: { fullName: '', email: '' },
  experience: [],
  education: [],
  skillGroups: [],
  languages: [],
  certifications: [],
}

export const useCVEditorStore = create<CVEditorState>()(
  devtools(
    subscribeWithSelector(
      immer((set, get) => ({
        // ---- Initial State ----
        cvId: null,
        cvData: EMPTY_CV_DATA,
        originalData: null,
        currentStep: 'personal',
        completedSteps: new Set<EditorStep>(),
        isDirty: false,
        isSaving: false,
        lastSavedAt: null,
        aiPanelOpen: false,

        // ---- Navigation ----
        setStep: (step) =>
          set((s) => { s.currentStep = step }),

        markStepCompleted: (step) =>
          set((s) => { s.completedSteps.add(step) }),

        nextStep: () =>
          set((s) => {
            const idx = STEP_ORDER.indexOf(s.currentStep)
            if (idx < STEP_ORDER.length - 1) {
              s.completedSteps.add(s.currentStep)
              s.currentStep = STEP_ORDER[idx + 1]
            }
          }),

        prevStep: () =>
          set((s) => {
            const idx = STEP_ORDER.indexOf(s.currentStep)
            if (idx > 0) {
              s.currentStep = STEP_ORDER[idx - 1]
            }
          }),

        // ---- Data Init ----
        initFromServer: (cvId, data) =>
          set((s) => {
            s.cvId = cvId
            s.cvData = data
            s.originalData = structuredClone(data)
            s.isDirty = false
          }),

        // ---- Personal Info ----
        updatePersonalInfo: (info) =>
          set((s) => {
            Object.assign(s.cvData.personalInfo, info)
            s.isDirty = true
          }),

        // ---- Experience ----
        addExperience: (exp) =>
          set((s) => {
            if (!s.cvData.experience) s.cvData.experience = []
            s.cvData.experience.push(exp)
            s.isDirty = true
          }),

        updateExperience: (id, patch) =>
          set((s) => {
            const exp = s.cvData.experience?.find((e) => e.id === id)
            if (exp) Object.assign(exp, patch)
            s.isDirty = true
          }),

        removeExperience: (id) =>
          set((s) => {
            s.cvData.experience = s.cvData.experience?.filter((e) => e.id !== id) || []
            s.isDirty = true
          }),

        reorderExperience: (fromIndex, toIndex) =>
          set((s) => {
            const items = s.cvData.experience || []
            const [moved] = items.splice(fromIndex, 1)
            items.splice(toIndex, 0, moved)
            s.isDirty = true
          }),

        // ---- Education ----
        addEducation: (edu) =>
          set((s) => {
            if (!s.cvData.education) s.cvData.education = []
            s.cvData.education.push(edu)
            s.isDirty = true
          }),

        updateEducation: (id, patch) =>
          set((s) => {
            const edu = s.cvData.education?.find((e) => e.id === id)
            if (edu) Object.assign(edu, patch)
            s.isDirty = true
          }),

        removeEducation: (id) =>
          set((s) => {
            s.cvData.education = s.cvData.education?.filter((e) => e.id !== id) || []
            s.isDirty = true
          }),

        // ---- Skills / Languages / Certs ----
        updateSkillGroups: (groups) =>
          set((s) => {
            s.cvData.skillGroups = groups
            s.isDirty = true
          }),

        updateLanguages: (langs) =>
          set((s) => {
            s.cvData.languages = langs
            s.isDirty = true
          }),

        updateCertifications: (certs) =>
          set((s) => {
            s.cvData.certifications = certs
            s.isDirty = true
          }),

        // ---- AI ----
        applyAIPatch: (patch) =>
          set((s) => {
            Object.assign(s.cvData, patch)
            s.isDirty = true
          }),

        // ---- Saving ----
        setSaving: (saving) =>
          set((s) => { s.isSaving = saving }),

        markSaved: () =>
          set((s) => {
            s.isDirty = false
            s.isSaving = false
            s.lastSavedAt = new Date()
            s.originalData = structuredClone(s.cvData)
          }),

        reset: () =>
          set((s) => {
            s.cvId = null
            s.cvData = EMPTY_CV_DATA
            s.originalData = null
            s.currentStep = 'personal'
            s.completedSteps = new Set()
            s.isDirty = false
            s.isSaving = false
            s.lastSavedAt = null
          }),
      }))
    ),
    { name: 'CVEditorStore', enabled: process.env.NODE_ENV === 'development' }
  )
)
```
