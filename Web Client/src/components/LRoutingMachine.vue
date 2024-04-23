<script>
import 'leaflet-routing-machine/dist/leaflet-routing-machine.css'
import L from 'leaflet'
import 'leaflet-routing-machine'

const props = {
  mapObject: {
    type: Object
  },
  visible: {
    type: Boolean,
    default: true
  },
  waypoints: {
    type: Array,
    required: true
  },
  router: {
    type: L.IRouter
  },
  plan: {
    type: L.Routing.Plan
  },
  geocoder: {
    type: L.IGeocoder
  },
  fitSelectedRoutes: {
    type: [String, Boolean],
    default: 'smart'
  },
  lineOptions: {
    type: L.LineOptions
  },
  routeLine: {
    type: Function
  },
  autoRoute: {
    type: Boolean,
    default: true
  },
  routeWhileDragging: {
    type: Boolean,
    default: false
  },
  routeDragInterval: {
    type: Number,
    default: 500
  },
  waypointMode: {
    type: String,
    default: 'connect'
  },
  useZoomParameter: {
    type: Boolean,
    default: false
  },
  showAlternatives: {
    type: Boolean,
    default: false
  },
  altLineOptions: {
    type: L.LineOptions
  }
}

export default {
  props,
  name: 'LRoutingMachine',
  data() {
    return {
      ready: false,
      map: null,
      layer: null
    }
  },
  watch: {
    mapObject() {
      if (this.mapObject == null) {
        return
      }
      this.add()
    }
  },
  mounted() {
    this.add()
  },
  beforeUnmount() {
    return this.layer ? this.layer.remove() : null
  },
  methods: {
    add() {
      if (this.mapObject == null) {
        return
      }

      const {
        waypoints,
        fitSelectedRoutes,
        autoRoute,
        routeWhileDragging,
        routeDragInterval,
        waypointMode,
        useZoomParameter,
        showAlternatives
      } = this

      const options = {
        waypoints,
        fitSelectedRoutes,
        autoRoute,
        routeWhileDragging,
        routeDragInterval,
        waypointMode,
        useZoomParameter,
        showAlternatives
      }

      const routingLayer = L.Routing.control(options)
      routingLayer.addTo(this.mapObject)
      this.layer = routingLayer

      this.ready = true
    }
  }
}
</script>
