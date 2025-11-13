console.log("Content script loaded!");

function handleIframe() {
  const speedgraderIframe = document.getElementById("speedgrader_iframe");
  if (speedgraderIframe) {
    console.log("Found speedgrader_iframe!");
    speedgraderIframe.addEventListener("load", () => {
      try {
        const innerDoc = speedgraderIframe.contentDocument;
        if (innerDoc) {
          const preview = innerDoc.getElementById("submission_preview");
          if (preview) {
            const p = preview.querySelector("p");
            if (p && p.textContent) {
              console.log("Found submission URL:", p.textContent.trim());
              chrome.storage.local.set({ submissionUrl: p.textContent.trim() });
            } else {
              console.log("No <p> found inside submission_preview.");
            }
          } else {
            console.log("No submission_preview found in iframe.");
          }
        } else {
          console.log("Iframe contentDocument not available.");
        }
      } catch (e) {
        console.log("Error accessing iframe:", e);
      }
    });
    return true;
  }
  return false;
}

// Try immediately, then observe if not found
if (!handleIframe()) {
  const observer = new MutationObserver(() => {
    if (handleIframe()) {
      observer.disconnect();
    }
  });
  observer.observe(document.body, { childList: true, subtree: true });
}