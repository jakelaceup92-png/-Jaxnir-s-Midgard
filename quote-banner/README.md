# Jaxnir Quote Banner

Standalone, dependency-free browser-source overlay for Meld Studio.

## Live behavior

- Rotates through 100 shuffled motivational quotes without repeating a quote until the deck is exhausted.
- After every two regular quotes, alternates between a Jaxnir/Prime/Extra Life support reminder and a social-account message.
- Cycles Twitch, YouTube, TikTok, and Discord messages so this banner can replace the separate social bar.
- Displays each message for nine seconds with a 600 ms exit and entry transition.
- Uses one persistent timer and safely resumes after browser-source visibility changes.
- Dynamically fits each message to the current browser-source dimensions with `ResizeObserver`.

## Meld setup

1. Add a web/browser-source layer.
2. Paste the GitHub Pages URL for the `quote-banner/` directory.
3. Resize the layer beneath the webcam. The visible banner fills the complete source bounds.
4. Keep the URL query string empty for normal nine-second timing.

For rapid testing only, append `?test=1` to use shorter timing.
