let toast = null;
document.addEventListener("DOMContentLoaded", () => {
  toast = new ToastNotifier({
    position: "top-right", // Default position
  });
});

/**
 *
 * @param {Event} event
 */
const handleSubmit = async (event) => {
  event.preventDefault();
  const form = event.target;
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());
  const submitBtn = form.querySelector("button[type='submit']");
  submitBtn.disabled = true;
  submitBtn.classList.add("disabled");

  if (!data.name || !data.email || !data.message || !data.subject) {
    toast.error("Please fill in all fields.");
    return;
  }
  const response = await fetch("/contact_team", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  if (response.ok) {
    toast.success("Message sent successfully!");
    form.reset();
  } else {
    toast.error("Failed to send message. Please try again later.");
  }
  submitBtn.disabled = false;
  submitBtn.classList.remove("disabled");
  return false;
};
