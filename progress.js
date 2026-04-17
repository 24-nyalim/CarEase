let table;
let toast;
let user_email = "";

let requestId = null;

const initiatePolling = () => {
  //initiate polling to check status
};

const handlePayment = (phone, appointment_id, amount) => {
  if (!phone) {
    toast.error("No phone number found. Please fetch appointments first.");
    return;
  }
  const formmatPhone = phone.replace("+", "");
  axios
    .post("/stk_push", {
      phone: formmatPhone,
      appointment_id: appointment_id,
      amount,
    })
    .then((response) => {
      console.log(response.data);
      toast.info("Please complete the payment on your phone.");
      getAppointMents();
    })
    .catch((error) => {
      console.error("Error during payment:", error);
      const serverError = error?.response?.data?.error;
      const details = error?.response?.data?.details;
      const detailText =
        typeof serverError === "string" && serverError.trim().length > 0
          ? ` ${serverError}`
          : typeof details === "string" && details.trim().length > 0
          ? ` ${details}`
          : "";
      toast.error(`Payment failed. Please try again.${detailText}`);
    })
    .finally(() => {});
};

document.addEventListener("DOMContentLoaded", function () {
  h = window.gridjs.h;
  toast = new ToastNotifier({
    position: "top-right", // Default position
  });

  table = new gridjs.Grid({
    columns: [
      {
        name: "Customer Name",
        formatter: (cell) => gridjs.html(`<strong>${cell}</strong>`),
      },
      "Email",
      "Service",
      "Appointment Date",
      "Status",
      "Price",
      {
        name: "Action",
        formatter: (cell, row) => {
          const unprocessed =
            row.cells[10].data.toLowerCase() === "unprocessed";
          const isPending = row.cells[10].data.toLowerCase() === "pending";
          const isPaid = row.cells[10].data.toLowerCase() === "completed";
          const isFailed = row.cells[10].data.toLowerCase() === "failed";
          return h(
            "button",
            {
              className: `pay-btn ${isPending ? "pending" : ""} ${
                isPaid ? "paid" : ""
              }`,
              /**
               *  @param {Event} event - The event object from form submission
               */
              onClick: (event) => {
                if (!unprocessed) return;
                event.target.classList.add("disabled");
                console.log(row);
                handlePayment(
                  row.cells[8].data,
                  row.cells[9].data,
                  row.cells[5].data
                );
              },
            },
            `${unprocessed ? "Pay Now" : ""} ${isPending ? "Pending" : ""} ${
              isPaid ? "Paid" : ""
            } ${isFailed ? "Failed" : ""}`
          );
        },
      },
      {
        name: "Service ID",
        hidden: true, // Hides the column but keeps data available
      },
      {
        name: "Receipt ID",
        hidden: true,
      },
      {
        name: "Phone",
        hidden: true,
      },
      {
        name: "Appointment ID",
        hidden: true,
      },
      {
        name: "Payment Status",
        hidden: true,
      },
    ],
    data: [],
    pagination: {
      enabled: true,
      limit: 5,
      summary: true,
    },
    with: "100%",
    sort: true,
  });

  table.render(document.getElementById("table-wrapper"));
});

const createTable = (data) => {
  table
    .updateConfig({
      with: "100%",
      data: data,
    })
    .forceRender();
};

const prepareTableData = (data) => {
  const tableData = data.map((appointment) => {
    const formattedDate = new Intl.DateTimeFormat("en-US", {
      month: "long",
      day: "numeric",
      year: "numeric",
    }).format(new Date(appointment.appointment_date ?? ""));
    phone = appointment.phone;

    return [
      appointment.customer_name,
      appointment.email,
      appointment.service_name,
      formattedDate,
      appointment.status,
      `$${appointment.service_price}`,
      appointment.service_id,
      appointment.receipt_id,
      appointment.phone,
      appointment.id,
      appointment.payment_status,
    ];
  });

  createTable(tableData);
};

const getAppointMents = () => {
  const submitBtn = document.querySelector(".submit-btn");

  axios
    .post("/get_appointments", { email_hash: user_email })
    .then((response) => {
      toast.success("Appointments fetched successfully!");
      console.log(response.data);
      prepareTableData(response.data);
    })
    .catch((error) => {
      console.error("Error fetching appointments:", error);
      toast.error("Failed to fetch appointments. Please try again.");
    })
    .finally(() => {
      submitBtn.classList.remove("disabled");
      submitBtn.disabled = false;
    });
};

/**
 *
 * @param {Event} event
 */
const handleSubmit = (event) => {
  event.preventDefault();
  const submitBtn = event.target.querySelector("button[type='submit']");
  submitBtn.classList.add("disabled");
  submitBtn.disabled = true;

  const data = Object.fromEntries(new FormData(event.target).entries());
  const email = data.email ?? "";

  if (!email.trim()) {
    toast.error("Please enter the code we sent to your email.");
    submitBtn.classList.remove("disabled");
    submitBtn.disabled = false;
    return;
  }

  user_email = email.trim();

  toast.info("Fetching appointments. Sit tight!");

  getAppointMents();
};
