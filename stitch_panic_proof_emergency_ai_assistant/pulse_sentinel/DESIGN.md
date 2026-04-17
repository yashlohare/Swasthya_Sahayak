# Design System Strategy: The Vital Pulse

## 1. Overview & Creative North Star
**Creative North Star: "Luminescent Urgency"**

In high-stakes emergency environments, a user’s cognitive load is at its breaking point. This design system rejects the cluttered, utility-first aesthetic of traditional medical software. Instead, it adopts a **"Luminescent Urgency"**—a philosophy that combines the authoritative clarity of high-end editorial design with the calming, tactile nature of glassmorphism.

We break the "template" look by utilizing intentional asymmetry and high-contrast typography scales. The layout is designed to feel "panic-proof," guiding the eye with soft glows and 3D orbs that act as visual anchors, ensuring that even in a state of distress, the next action is never in doubt.

---

## 2. Colors & Chromatic Hierarchy
Our palette moves beyond simple status indicators. It uses deep, vibrating reds and oranges to command attention, balanced by a sophisticated dark-mode architecture.

### The "No-Line" Rule
To maintain a premium, seamless feel, **1px solid borders are strictly prohibited for sectioning.** Structural boundaries must be defined solely through:
- **Background Shifts:** Placing a `surface-container-low` component against a `surface` background.
- **Tonal Transitions:** Using subtle shifts between container tiers to imply depth.

### Surface Hierarchy & Nesting
Treat the UI as a physical stack of semi-transparent layers. 
- Use `surface-container-lowest` (#000000) for the deepest background layer.
- Layer `surface-container` (#19191c) or `surface-container-high` (#1f1f22) to create "nested" zones of information. Each inner container should feel like a more focused sheet of glass resting atop the layer below.

### The "Glass & Gradient" Rule
Floating elements (Modals, Action Sheets) must utilize **Glassmorphism**.
- **Fill:** Use `surface-variant` (#252528) at 60-80% opacity.
- **Effect:** Apply a `backdrop-blur` (20px-40px). 
- **Signature Texture:** Primary CTAs should not be flat. Use a linear gradient from `primary` (#ff8f70) to `primary-container` (#ff7852) to provide a "living" energy to the button.

---

## 3. Typography: The Voice of Authority
We employ a dual-font strategy to balance impact with legibility.

- **Display & Headlines (Manrope):** Chosen for its geometric modernism. Large scales (`display-lg` at 3.5rem) should be used for critical status updates. Bold weights are the default for headlines to ensure they "pop" against dark backgrounds.
- **Body & Labels (Inter):** The workhorse for high-readability. Inter’s tall x-height ensures that medical instructions are legible even if the user is in motion or has blurred vision.

**Hierarchy as Identity:** 
Use extreme contrast in scale. A `display-md` headline next to a `body-md` description creates an editorial "big-type" feel that feels intentional and premium rather than a generic grid of text.

---

## 4. Elevation & Depth: Tonal Layering
Traditional drop shadows are too "dirty" for this aesthetic. We achieve depth through light and layering.

- **The Layering Principle:** Stack `surface-container` tiers. A `surface-container-highest` card on a `surface-low` background provides enough "lift" to be perceived without a shadow.
- **Ambient Shadows:** For floating elements, use a "glow-shadow." The shadow color should be a 10% opacity version of the `primary` or `secondary` token, with a blur radius of 40px+. This mimics a light-emitting source rather than a physical shadow.
- **The "Ghost Border" Fallback:** If a container needs more definition against a complex background, use a **Ghost Border**: `outline-variant` (#48474a) at 20% opacity.
- **3D Orbs:** Use radial gradients of `tertiary_container` (#007aff) or `secondary` (#fe9400) behind glass layers to create a sense of three-dimensional space and "AI presence."

---

## 5. Components

### Buttons
- **Primary:** High-impact gradients (`primary` to `primary_container`). Large touch targets (minimum 56px height). Roundedness: `xl` (1.5rem) for a friendly, tactile feel.
- **Secondary:** Glass-filled (`surface_bright` at 20% opacity) with `on_surface` text.
- **Tertiary:** No background, `primary` colored text, bold weight.

### Input Fields
- **Panic-Proof Design:** No thin outlines. Use a `surface_container_highest` background with a `sm` (0.25rem) bottom-heavy accent of `primary` only when focused. 
- **Error State:** The field should pulse with an `error_container` (#a70138) glow rather than just turning text red.

### Cards & Lists
- **No Divider Lines:** Use vertical white space (1.5rem+) or a background shift to `surface_container_low` to separate items.
- **Interaction:** Cards should have a subtle "scale up" (1.02x) on press to provide haptic-visual feedback.

### The "Vital Pulse" Orb (Custom Component)
- A 3D animated sphere using `tertiary` (#679cff) glows. This serves as the AI's "listening" state. It should appear to sit *behind* the glass interface, blurred and ethereal.

---

## 6. Do’s and Don'ts

### Do:
- **Use Large Touch Targets:** Every interactive element must be easily tappable by someone with shaking hands (minimum 48x48dp).
- **Embrace High Contrast:** Ensure `on_background` white text is used against the deep `background` black for maximum readability.
- **Use "Breathing" Gradients:** Apply very subtle, slow-moving mesh gradients in the background to prevent the UI from feeling "dead."

### Don't:
- **Don't Use Dividers:** Avoid horizontal lines between list items; they add visual noise that increases panic.
- **Don't Use Pure Gray Shadows:** Standard `#000000` shadows look muddy on dark themes. Always tint your shadows with the background or primary hue.
- **Don't Use "Standard" Weights:** In an emergency, thin fonts disappear. Stick to Medium, Semi-Bold, and Bold for critical information.
- **Don't Over-Animate:** Animations should be functional (guiding the eye) rather than decorative. Avoid long durations; use "snappy" easings (e.g., cubic-bezier(0.2, 0.8, 0.2, 1)).