// Clerk Frontend Integration Helper
// Usage in HTML:
// <script async crossorigin="anonymous" data-clerk-publishable-key="pk_test_..." src="https://cdn.jsdelivr.net/npm/@clerk/clerk-js@latest/dist/clerk.browser.js" type="text/javascript"></script>

export async function initClerk(publishableKey) {
  const key = publishableKey || window.__CLERK_PUBLISHABLE_KEY__;
  if (!key) {
    console.error("Clerk Publishable Key not found.");
    return null;
  }
  
  if (window.Clerk) {
    await window.Clerk.load();
    return window.Clerk;
  }
  return null;
}
