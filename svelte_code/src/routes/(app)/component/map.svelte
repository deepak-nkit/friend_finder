<script lang="ts">
  import { onMount } from "svelte";

  export let latitude: null | number = null;
  export let longitutde: null | number = null;

  let leaflet;
  onMount(async () => {
    const L = await import("leaflet");
    leaflet = L.default;

    var map = L.map("map").setView([20.5937, 78.9629], 15);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
      attribution:
        'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
    }).addTo(map);

    var marker = L.marker([22.309425, 72.13623])
      .addTo(map)
      .bindPopup("<b>Here!</b><br>INDIA")
      .openPopup();

    map.locate({ setView: true, maxZoom: 19 });

    function onLocationFound(e) {
      var radius = e.accuracy;
      latitude = e.latlng["lat"];
      longitutde = e.latlng["lng"];

      console.log("**", e.latlng);
      L.marker(e.latlng)
        .addTo(map)
        .bindPopup("You are within " + radius + " meters from this point")
        .openPopup();

      var marker = L.marker(e.latlng)
        .addTo(map)
        .bindPopup("<b>Hey!</b><br>Your loc")
        .openPopup();

    }

    function onLocationError(e) {
      alert(e.message);
    }
    map.on("locationfound", onLocationFound);
    var popup = L.popup();
    function onMapClick(e) {
      popup
        .setLatLng(e.latlng)
        .setContent("You clicked the map at " + e.latlng.toString())
        .openOn(map);
    }
    map.on("click", onMapClick);
  });

  function updateCoordinates(newLat: number, newLng: number) {
    console.log("--", newLat, newLng);
    coordinates.set({ lat: newLat, lng: newLng });
  }
</script>

<link
  rel="stylesheet"
  href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
  integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY="
  crossorigin=""
/>

<div class="max-w-[700px] max-h-[900px] md:mt-3">
  <div class="border-1 w-[700px] h-[600px]" id="map"></div>
</div>
