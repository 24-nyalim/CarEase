let socket = null;
let isWatching = false;
let marker = null;
let map = null;

document.addEventListener("DOMContentLoaded", () => {
  // Initialize the map
  map = L.map("map").setView([51.505, -0.09], 13); // Initial position

  // Add a tile layer (OpenStreetMap in this case)
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution:
      '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);

  // Add a marker at the initial position
  marker = L.marker([51.505, -0.09]).addTo(map);
});

const updateMarker = (lat, lon) => {
  marker.setLatLng([lat, lon]); // Update the marker position
  map.panTo(new L.LatLng(lat, lon)); // Optionally, pan the map to the new location
};

const watchLocation = () => {
  if (isWatching) return; // Prevent multiple calls
  navigator.geolocation.watchPosition(
    (position) => {
      isWatching = true; // Set the flag to true when watching location
      const { latitude, longitude } = position.coords;
      console.log("Latitude:", latitude, "Longitude:", longitude);
      // You can send this data to your server or use it as needed
      socket.emit(
        "message",
        JSON.stringify({
          latitude,
          longitude,
        })
      );
    },
    (error) => {
      console.error("Error getting location:", error);
    },
    {
      enableHighAccuracy: false,
      maximumAge: 5000,
      timeout: 30000,
    }
  );
};

function generateAndEmitRandomLocation() {
  const latitude = Math.random() * 180 - 90; // Latitude: -90 to 90
  const longitude = Math.random() * 360 - 180; // Longitude: -180 to 180

  const locationData = {
    latitude: latitude,
    longitude: longitude,
  };

  socket.emit("message", JSON.stringify(locationData));

  console.log("Emitted:", locationData); // Optional: Log the emitted data
}

/**
 * @param {Event} event
 */
async function sendMessage(event) {
  if (!socket) {
    console.log("Socket not connected");
    return;
  }
  // generateAndEmitRandomLocation();
  // return;
  navigator.geolocation.getCurrentPosition(
    (position) => {
      const { latitude, longitude } = position.coords;
      console.log("Latitude:", latitude, "Longitude:", longitude);
      socket.emit(
        "message",
        JSON.stringify({
          latitude,
          longitude,
        })
      );
    },
    (error) => {
      console.error("Error getting location:", error);
    },
    {
      enableHighAccuracy: false,
      maximumAge: 5000,
      timeout: 30000,
    }
  );
}

/**
 *
 * @param {Event} event
 */
async function connectSocket(event) {
  const button = event.target;
  button.innerText = "Connecting...";
  // Create a Socket.IO client connection
  socket = io(`${window.location.origin}/track_navigator`); // Adjust the URL based on your server

  socket.on("connect", () => {
    console.log("Connected to WebSocket server");
    button.innerText = "Connected!";
    button.disabled = true;
    watchLocation(); // Start watching the location after connecting
  });

  socket.on("message", (data) => {
    const parsedData = JSON.parse(data);
    console.log("Received:", parsedData);
    updateMarker(parsedData.latitude, parsedData.longitude); // Update the marker position on the map
  });

  socket.on("disconnect", () => {
    button.innerText = "Error!";
    button.disabled = false;
    console.log("Disconnected from WebSocket server");
  });
}
