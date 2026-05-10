# Issues Found

---

## BUG-001 — Select Plan Page: Incorrect Addon Cards Pre-Selected for MRI Scan Encounters

**Page:** Booking — Select Plan  
**Severity:** High  
**Status:** Open

### Description
Selecting any MRI scan encounter card causes both the **"Lungs CT Scan"** and **"Heart CT Scan"** addon cards to be selected automatically.

### Steps to Reproduce
1. Navigate to the Select Plan page.
2. Click any MRI scan encounter card (e.g. "MRI Scan", "MRI Scan with Spine", etc.).

### Expected Behavior
Addon cards for the proper scan should be selected.

### Actual Behavior
Both "Lungs CT Scan" and "Heart CT Scan" addon cards are automatically selected.

---

## BUG-002 — Select Plan Page: Selecting Heart CT Scan Removes All Addon Cards

**Page:** Booking — Select Plan  
**Severity:** High  
**Status:** Open

### Description
When the user selects the **"Heart CT Scan"** encounter card, all addon cards are removed from view.

### Steps to Reproduce
1. Navigate to the Select Plan page.
2. Click the "Heart CT Scan" encounter card.

### Expected Behavior
Relevant addon cards should remain visible.

### Actual Behavior
All addon cards disappear from the page.

---

## BUG-003 — Select Plan Page: Selecting Lungs CT Scan Displays Heart CT Scan as Addon

**Page:** Booking — Select Plan  
**Severity:** Medium  
**Status:** Open

### Description
When the user selects the **"Lungs CT Scan"** encounter card, the **"Heart CT Scan"** addon card is displayed.

### Steps to Reproduce
1. Navigate to the Select Plan page.
2. Click the "Lungs CT Scan" encounter card.

### Expected Behavior
Only addons relevant to the Lungs CT Scan should be displayed.

### Actual Behavior
The "Heart CT Scan" addon card appears, which is unrelated to a Lungs CT Scan selection.
