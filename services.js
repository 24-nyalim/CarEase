const formatPhoneNumber = (phoneNumber) => {
  if (phoneNumber.startsWith("0")) {
    //remove leading zero and replce with +254
    return phoneNumber.replace(/^0/, "+254");
  } else {
    return false;
  }
};

/**
 * Handles form submission
 * @param {Event} event - The event object from form submission
 */
const handleSubmit = async (event) => {
  event.preventDefault();
  const submitBtn = event.target.querySelector("button[type='submit']");
  submitBtn.classList.add("disabled");
  submitBtn.disabled = true;

  const toast = new ToastNotifier({
    position: "top-right", // Default position
  });

  const data = Object.fromEntries(new FormData(event.target).entries());

  if (
    !data.start_date ||
    !data.service ||
    !data.name ||
    !data.email ||
    !data.phone
  ) {
    toast.error("Please fill in all required fields.");
    submitBtn.classList.remove("disabled");
    submitBtn.disabled = false;
    return;
  }

  if (data.phone.length !== 10) {
    toast.error("Please provide a valid phone number.");
    submitBtn.classList.remove("disabled");
    submitBtn.disabled = false;
    return;
  }

  const formattedPhoneNumber = formatPhoneNumber(data.phone);
  if (!formattedPhoneNumber) {
    toast.error("Please provide a valid phone number.");
    submitBtn.classList.remove("disabled");
    submitBtn.disabled = false;
    return;
  }

  // Get the select element
  const selectElement = document.querySelector('select[name="service"]');
  // Find the selected option
  const selectedOption = selectElement.querySelector(
    `option[value="${data.service}"]`
  );
  const serviceName = selectedOption ? selectedOption.text : "";

  const name = data.name ?? "";
  const email = data.email ?? "";
  const start_date = new Date(data.start_date ?? "").toISOString();
  const end_date = new Date(
    new Date(start_date).setHours(new Date(start_date).getHours() + 2)
  ).toISOString();
  const service = data.service ?? "";
  const special_request = data.special_request ?? "";
  const legible_date = new Intl.DateTimeFormat("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric",
  }).format(new Date(data.start_date ?? ""));

  const formData = {
    name,
    email,
    start_date,
    end_date,
    service,
    special_request,
    legible_date,
    service_name: serviceName,
    phone: formattedPhoneNumber,
  };
  const jsonData = JSON.stringify(formData);

  /** @type {import('axios').AxiosInstance} */
  axios
    .post("/create_booking", jsonData, {
      headers: {
        "Content-Type": "application/json",
      },
    })
    .then((response) => {
      const emailSent = response?.data?.email_sent === true;
      const emailError = response?.data?.email_error;
      if (emailSent) {
        toast.success("Successfully booked an appointment. Check your email!");
      } else {
        toast.success("Appointment booked successfully.");
        const detailedError =
          typeof emailError === "string" && emailError.trim().length > 0
            ? ` Reason: ${emailError}`
            : "";
        toast.error(
          `Booking saved, but we could not send the email confirmation right now.${detailedError}`
        );
      }

      console.log(response.data);
    })
    .catch((error) => {
      const serverError = error?.response?.data?.error;
      const detailedError =
        typeof serverError === "string" && serverError.trim().length > 0
          ? ` ${serverError}`
          : "";
      toast.error(`Error creating booking. Please try again.${detailedError}`);
      console.error(error);
    })
    .finally(() => {
      submitBtn.classList.remove("disabled");
      submitBtn.disabled = false;
    });
};

/**
 * @param {Event} event - The event object from the change event
 */
const handleServiceChange = (event) => {
  const selectedOption = event.target.options[event.target.selectedIndex];
  const price = selectedOption.getAttribute("data-price");
  if (!price) {
    return;
  }
  const balanceEl = document.querySelector(".balance-span-txt");
  const totalEl = document.querySelector(".tot-span-txt");
  const vatEl = document.querySelector(".vat-span-txt");
  const vat = 0.12 * parseFloat(price); // calculate VAT at 12%
  const total = 1.12 * parseFloat(price); // multiply by tax rate of 12%

  balanceEl.innerText = `$ ${price}`;
  totalEl.innerText = `$ ${total.toFixed(2)}`;
  vatEl.innerText = `$ ${vat.toFixed(2)}`; // Display the VAT amount

  // Add any additional logic to handle the change event here
};
