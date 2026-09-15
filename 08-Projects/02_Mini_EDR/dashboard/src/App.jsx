import { useEffect, useMemo, useState } from "react";

import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

import "./App.css";

const API_BASE = "http://localhost:8000";


// =========================
// DATA HELPERS
// =========================

function getEventTypeData(events) {
  const counts = {};

  events.forEach((event) => {
    const type = event.event_type || "unknown";
    counts[type] = (counts[type] || 0) + 1;
  });

  return Object.entries(counts)
    .map(([type, count]) => ({
      type,
      count,
    }))
    .sort((a, b) => b.count - a.count);
}


function getSeverityData(events) {
  const counts = {
    INFO: 0,
    MEDIUM: 0,
    HIGH: 0,
  };

  events.forEach((event) => {
    const severity = event.severity || "INFO";

    if (counts[severity] !== undefined) {
      counts[severity]++;
    }
  });

  return Object.entries(counts)
    .filter(([, count]) => count > 0)
    .map(([severity, count]) => ({
      severity,
      count,
    }));
}


function getDetectionRuleData(events) {
  const counts = {};

  events
    .filter((event) => event.event_category === "detection")
    .forEach((event) => {
      const rule = event.rule || "Unknown";

      counts[rule] = (counts[rule] || 0) + 1;
    });

  return Object.entries(counts)
    .map(([rule, count]) => ({
      rule,
      count,
    }))
    .sort((a, b) => b.count - a.count);
}


function getTopProcessData(events) {
  const counts = {};

  events.forEach((event) => {
    const details = event.details || {};

    let process = details.process;

    if (!process && details.evidence) {
      process = details.evidence.process;
    }

    if (!process) {
      return;
    }

    counts[process] = (counts[process] || 0) + 1;
  });

  return Object.entries(counts)
    .map(([process, count]) => ({
      process,
      count,
    }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 8);
}


function getEventTimeline(events) {
  const counts = {};

  events.forEach((event) => {
    if (!event.timestamp) {
      return;
    }

    const time = event.timestamp.substring(11, 16);

    counts[time] = (counts[time] || 0) + 1;
  });

  return Object.entries(counts)
    .sort(([timeA], [timeB]) => timeA.localeCompare(timeB))
    .map(([time, count]) => ({
      time,
      count,
    }));
}


// =========================
// EVENT DISPLAY HELPERS
// =========================

function getEventTitle(event) {
  if (event.event_type === "process_created") {
    return event.details?.name || "Process Created";
  }

  if (event.event_type === "network_connection") {
    return event.details?.process || "Network Connection";
  }

  if (
    event.event_type === "file_created" ||
    event.event_type === "file_modified" ||
    event.event_type === "file_deleted"
  ) {
    return event.details?.file_name || event.event_type;
  }

  if (
    event.event_type === "file_integrity_changed" ||
    event.event_type === "file_integrity_deleted"
  ) {
    return event.details?.file_name || event.event_type;
  }

  if (event.event_type === "detection") {
    return event.detection || "Detection Alert";
  }

  return event.event_type || "Unknown Event";
}


function getEventClass(event) {
  if (event.event_category === "detection") {
    return "event-detection";
  }

  if (event.event_type === "network_connection") {
    return "event-network";
  }

  if (
    event.event_type === "file_created" ||
    event.event_type === "file_modified" ||
    event.event_type === "file_deleted"
  ) {
    return "event-file";
  }

  if (
    event.event_type === "file_integrity_changed" ||
    event.event_type === "file_integrity_deleted"
  ) {
    return "event-integrity";
  }

  return "event-process";
}


function formatValue(value) {
  if (value === null || value === undefined) {
    return "N/A";
  }

  if (typeof value === "object") {
    return JSON.stringify(value, null, 2);
  }

  return String(value);
}


// =========================
// APP
// =========================

function App() {
  const [events, setEvents] = useState([]);
  const [incidents, setIncidents] = useState([]);

  const [loading, setLoading] = useState(true);
  const [apiOnline, setApiOnline] = useState(false);

  const [expandedEventId, setExpandedEventId] = useState(null);
  const [showAllEvents, setShowAllEvents] = useState(false);

  const [activeFilter, setActiveFilter] = useState("all");
  const [searchTerm, setSearchTerm] = useState("");


  // =========================
  // FETCH DATA
  // =========================

  const fetchData = async () => {
    try {
      const [eventsResponse, incidentsResponse] =
        await Promise.all([
          fetch(`${API_BASE}/api/events`),
          fetch(`${API_BASE}/api/incidents`),
        ]);

      if (
        !eventsResponse.ok ||
        !incidentsResponse.ok
      ) {
        throw new Error("API request failed");
      }

      const eventsData =
        await eventsResponse.json();

      const incidentsData =
        await incidentsResponse.json();

      setEvents(
        Array.isArray(eventsData)
          ? eventsData
          : []
      );

      setIncidents(
        Array.isArray(incidentsData)
          ? incidentsData
          : []
      );

      setApiOnline(true);
      setLoading(false);
    } catch (error) {
      console.error(
        "Failed to fetch EDR data:",
        error
      );

      setApiOnline(false);
      setLoading(false);
    }
  };


  // =========================
  // AUTO REFRESH
  // =========================

  useEffect(() => {
    fetchData();

    const interval = setInterval(
      fetchData,
      2000
    );

    return () => clearInterval(interval);
  }, []);


  // =========================
  // STATISTICS
  // =========================

  const totalEvents = events.length;

  const totalAlerts = events.filter(
    (event) =>
      event.event_category === "detection"
  ).length;

  const highSeverity = events.filter(
    (event) =>
      event.severity === "HIGH"
  ).length;

  const totalIncidents =
    incidents.length;


  // =========================
  // FILTER EVENTS
  // =========================

  const filteredEvents = useMemo(() => {
    let result = [...events];

    if (activeFilter !== "all") {
      result = result.filter((event) => {
        switch (activeFilter) {
          case "process":
            return (
              event.event_type ===
                "process_created" ||
              event.event_type ===
                "process_terminated"
            );

          case "network":
            return (
              event.event_type ===
              "network_connection"
            );

          case "file":
            return (
              event.event_type ===
                "file_created" ||
              event.event_type ===
                "file_modified" ||
              event.event_type ===
                "file_deleted"
            );

          case "integrity":
            return (
              event.event_type ===
                "file_integrity_changed" ||
              event.event_type ===
                "file_integrity_deleted"
            );

          case "detection":
            return (
              event.event_category ===
              "detection"
            );

          default:
            return true;
        }
      });
    }

    if (searchTerm.trim()) {
      const search =
        searchTerm.toLowerCase();

      result = result.filter((event) =>
        JSON.stringify(event)
          .toLowerCase()
          .includes(search)
      );
    }

    return result;
  }, [
    events,
    activeFilter,
    searchTerm,
  ]);


  // =========================
  // RECENT EVENTS
  // =========================

  const recentEvents = useMemo(() => {
    const orderedEvents = [...filteredEvents].reverse();

    return showAllEvents
      ? orderedEvents
      : orderedEvents.slice(0, 10);
  }, [filteredEvents, showAllEvents]);


  // =========================
  // ANALYTICS
  // =========================

  const eventTypeData =
    getEventTypeData(events);

  const severityData =
    getSeverityData(events);

  const detectionRuleData =
    getDetectionRuleData(events);

  const topProcessData =
    getTopProcessData(events);

  const eventTimeline =
    getEventTimeline(events);


  // =========================
  // SEVERITY COLORS
  // =========================

  const getSeverityColor = (
    severity
  ) => {
    if (severity === "HIGH") {
      return "#ef4444";
    }

    if (severity === "MEDIUM") {
      return "#f59e0b";
    }

    return "#22c55e";
  };


  // =========================
  // DETECTION CHART SCALE
  // =========================

  const detectionMax =
    detectionRuleData.length > 0
      ? Math.max(
          ...detectionRuleData.map(
            (item) => item.count
          )
        )
      : 0;

  const detectionYAxisMax =
    Math.max(2, detectionMax + 1);


  // =========================
  // RENDER
  // =========================

  return (
    <div className="dashboard">

      {/* =========================
          HEADER
          ========================= */}

      <header className="dashboard-header">

        <div>
          <h1>Mini EDR</h1>

          <p>
            Endpoint Detection &amp;
            Response Dashboard
          </p>
        </div>

        <div
          className={`api-status ${
            apiOnline
              ? "online"
              : "offline"
          }`}
        >
          <span className="status-dot"></span>

          {apiOnline
            ? "EDR Active"
            : "API Offline"}
        </div>

      </header>


      {/* =========================
          STATISTICS
          ========================= */}

      <section className="stats-grid">

        <div className="stat-card">

          <span className="stat-label">
            Total Events
          </span>

          <strong className="stat-value blue">
            {totalEvents}
          </strong>

        </div>


        <div className="stat-card">

          <span className="stat-label">
            Total Alerts
          </span>

          <strong className="stat-value red">
            {totalAlerts}
          </strong>

        </div>


        <div className="stat-card">

          <span className="stat-label">
            High Severity
          </span>

          <strong className="stat-value danger">
            {highSeverity}
          </strong>

        </div>


        <div className="stat-card">

          <span className="stat-label">
            Incidents
          </span>

          <strong className="stat-value purple">
            {totalIncidents}
          </strong>

        </div>

      </section>


      {/* =========================
          ANALYTICS
          ========================= */}

      <section className="analytics-grid">

        {/* =========================
            SEVERITY DISTRIBUTION
            ========================= */}

        <div className="panel chart-panel">

          <div className="panel-header">

            <h2>
              Severity Distribution
            </h2>

            <span>
              Event Severity
            </span>

          </div>

          <div className="chart-container">

            {severityData.length > 0 ? (

              <ResponsiveContainer
                width="100%"
                height="100%"
              >

                <PieChart>

                  <Pie
                    data={severityData}
                    dataKey="count"
                    nameKey="severity"
                    cx="50%"
                    cy="50%"
                    innerRadius={65}
                    outerRadius={95}
                    paddingAngle={3}
                    label
                  >

                    {severityData.map(
                      (entry) => (

                        <Cell
                          key={`severity-${entry.severity}`}
                          fill={getSeverityColor(
                            entry.severity
                          )}
                        />

                      )
                    )}

                  </Pie>

                  <Tooltip />

                </PieChart>

              </ResponsiveContainer>

            ) : (

              <div className="no-data">
                No severity data
              </div>

            )}

          </div>

        </div>


        {/* =========================
            EVENTS BY TYPE
            ========================= */}

        <div className="panel chart-panel">

          <div className="panel-header">

            <h2>
              Events by Type
            </h2>

            <span>
              Event Categories
            </span>

          </div>

          <div className="chart-container">

            {eventTypeData.length > 0 ? (

              <ResponsiveContainer
                width="100%"
                height="100%"
              >

                <BarChart
                  data={eventTypeData}
                  margin={{
                    top: 10,
                    right: 10,
                    left: 0,
                    bottom: 45,
                  }}
                >

                  <CartesianGrid
                    strokeDasharray="3 3"
                  />

                  <XAxis
                    dataKey="type"
                    angle={-35}
                    textAnchor="end"
                    interval={0}
                  />

                  <YAxis
                    label={{
                      value:
                        "Number of Events",
                      angle: -90,
                      position:
                        "insideLeft",
                      fill: "#94a3b8",
                      fontSize: 10,
                    }}
                  />

                  <Tooltip />

                  <Bar
                    dataKey="count"
                    fill="#38bdf8"
                    radius={[
                      4,
                      4,
                      0,
                      0,
                    ]}
                  />

                </BarChart>

              </ResponsiveContainer>

            ) : (

              <div className="no-data">
                No event data
              </div>

            )}

          </div>

        </div>


        {/* =========================
            EVENTS OVER TIME
            ========================= */}

        <div className="panel chart-panel wide">

          <div className="panel-header">

            <h2>
              Events Over Time
            </h2>

            <span>
              Event Activity
            </span>

          </div>

          <div className="chart-container">

            {eventTimeline.length > 0 ? (

              <ResponsiveContainer
                width="100%"
                height="100%"
              >

                <LineChart
                  data={eventTimeline}
                  margin={{
                    top: 15,
                    right: 15,
                    left: 15,
                    bottom: 20,
                  }}
                >

                  <CartesianGrid
                    strokeDasharray="3 3"
                  />

                  <XAxis
                    dataKey="time"
                    label={{
                      value: "Time",
                      position:
                        "insideBottom",
                      offset: -10,
                      fill: "#94a3b8",
                      fontSize: 11,
                    }}
                  />

                  <YAxis
                    allowDecimals={false}
                    label={{
                      value:
                        "Number of Events",
                      angle: -90,
                      position:
                        "insideLeft",
                      fill: "#94a3b8",
                      fontSize: 11,
                    }}
                  />

                  <Tooltip />

                  <Line
                    type="monotone"
                    dataKey="count"
                    stroke="#22d3ee"
                    strokeWidth={3}
                    dot={{
                      r: 4,
                      fill: "#22d3ee",
                      stroke:
                        "#e0f2fe",
                      strokeWidth: 2,
                    }}
                    activeDot={{
                      r: 6,
                    }}
                  />

                </LineChart>

              </ResponsiveContainer>

            ) : (

              <div className="no-data">
                No timeline data
              </div>

            )}

          </div>

        </div>


        {/* =========================
            DETECTION RULES
            ========================= */}

        <div className="panel chart-panel">

          <div className="panel-header">

            <h2>
              Detection Rules
            </h2>

            <span>
              Alert Frequency
            </span>

          </div>

          <div className="chart-container">

            {detectionRuleData.length > 0 ? (

              <ResponsiveContainer
                width="100%"
                height="100%"
              >

                <BarChart
                  data={detectionRuleData}
                  margin={{
                    top: 25,
                    right: 15,
                    left: 15,
                    bottom: 30,
                  }}
                >

                  <CartesianGrid
                    strokeDasharray="3 3"
                  />

                  <XAxis
                    dataKey="rule"
                    label={{
                      value:
                        "Detection Rule",
                      position:
                        "insideBottom",
                      offset: -15,
                      fill: "#94a3b8",
                      fontSize: 10,
                    }}
                  />

                  <YAxis
                    allowDecimals={false}
                    domain={[
                      0,
                      detectionYAxisMax,
                    ]}
                    label={{
                      value:
                        "Number of Alerts",
                      angle: -90,
                      position:
                        "insideLeft",
                      fill: "#94a3b8",
                      fontSize: 10,
                    }}
                  />

                  <Tooltip />

                  <Bar
                    dataKey="count"
                    fill="#a78bfa"
                    radius={[
                      4,
                      4,
                      0,
                      0,
                    ]}
                    label={{
                      position: "top",
                      fill: "#e2e8f0",
                      fontSize: 11,
                      fontWeight: 700,
                    }}
                  />

                </BarChart>

              </ResponsiveContainer>

            ) : (

              <div className="no-data">
                No detection rules triggered
              </div>

            )}

          </div>

        </div>


        {/* =========================
            TOP PROCESSES
            ========================= */}

        <div className="panel chart-panel">

          <div className="panel-header">

            <h2>
              Top Processes
            </h2>

            <span>
              Process Activity
            </span>

          </div>

          <div className="chart-container">

            {topProcessData.length > 0 ? (

              <ResponsiveContainer
                width="100%"
                height="100%"
              >

                <BarChart
                  layout="vertical"
                  data={topProcessData}
                  margin={{
                    top: 5,
                    right: 15,
                    left: 20,
                    bottom: 5,
                  }}
                >

                  <CartesianGrid
                    strokeDasharray="3 3"
                  />

                  <XAxis
                    type="number"
                    allowDecimals={false}
                    label={{
                      value:
                        "Number of Events",
                      position:
                        "insideBottom",
                      offset: -3,
                      fill: "#94a3b8",
                      fontSize: 10,
                    }}
                  />

                  <YAxis
                    type="category"
                    dataKey="process"
                    width={75}
                  />

                  <Tooltip />

                  <Bar
                    dataKey="count"
                    fill="#60a5fa"
                    radius={[
                      0,
                      4,
                      4,
                      0,
                    ]}
                  />

                </BarChart>

              </ResponsiveContainer>

            ) : (

              <div className="no-data">
                No process data
              </div>

            )}

          </div>

        </div>

      </section>


      {/* =========================
          MAIN GRID
          ========================= */}

      <section className="main-grid">

        {/* =========================
            RECENT ALERTS
            ========================= */}

        <div className="panel">

          <div className="panel-header">

            <h2>
              Recent Alerts
            </h2>

            <span>
              {totalAlerts} Total Alerts
            </span>

          </div>

          <div className="alert-list">

            {events
              .filter(
                (event) =>
                  event.event_category ===
                  "detection"
              )
              .reverse()
              .map((alert) => (

                <div
                  className={`alert-item ${
                    alert.severity ===
                    "HIGH"
                      ? "alert-high"
                      : alert.severity ===
                        "MEDIUM"
                      ? "alert-medium"
                      : "alert-info"
                  }`}
                  key={alert.event_id}
                >

                  <div className="alert-main">

                    <span className="rule-badge">
                      {alert.rule ||
                        "ALERT"}
                    </span>

                    <strong>
                      {alert.detection ||
                        "Detection Alert"}
                    </strong>

                  </div>

                  <div className="alert-meta">

                    <span
                      className={`severity-badge ${(
                        alert.severity ||
                        "INFO"
                      ).toLowerCase()}`}
                    >
                      {alert.severity ||
                        "INFO"}
                    </span>

                    <span>
                      {alert.timestamp ||
                        ""}
                    </span>

                  </div>

                </div>

              ))}

            {totalAlerts === 0 && (
              <div className="empty-state">
                No alerts detected
              </div>
            )}

          </div>

        </div>


        {/* =========================
            INCIDENTS
            ========================= */}

        <div className="panel">

          <div className="panel-header">

            <h2>
              Incidents
            </h2>

            <span>
              {totalIncidents} Total
              Incidents
            </span>

          </div>

          <div className="incident-list">

            {incidents
              .slice()
              .reverse()
              .map((incident) => (

                <div
                  className="incident-item"
                  key={
                    incident.incident_id
                  }
                >

                  <div className="incident-main">

                    <span className="incident-id">
                      {
                        incident.incident_id
                      }
                    </span>

                    <strong>
                      {incident.detection ||
                        "Security Incident"}
                    </strong>

                  </div>

                  <div className="incident-meta">

                    <span className="severity-badge high">
                      {incident.severity ||
                        "HIGH"}
                    </span>

                    <span>
                      {incident.status ||
                        "NEW"}
                    </span>

                  </div>

                </div>

              ))}

            {totalIncidents === 0 && (
              <div className="empty-state">
                No incidents created
              </div>
            )}

          </div>

        </div>


        {/* =========================
            RECENT EVENT ACTIVITY
            ========================= */}

        <div className="panel wide">

          <div className="panel-header">

            <div>

              <h2>
                Recent Event Activity
              </h2>

              <span>
                Click an event to view
                details
              </span>

            </div>

            <div className="event-header-actions">
              <div className="event-count">
                {filteredEvents.length} Events
              </div>

              {filteredEvents.length > 10 && (
                <button
                  className="view-all-events-button"
                  onClick={() => setShowAllEvents((current) => !current)}
                >
                  {showAllEvents ? "Show Recent" : "View All Events"}
                </button>
              )}
            </div>

          </div>


          {/* FILTERS */}

          <div className="filter-row">

            {[
              ["all", "All"],
              ["process", "Process"],
              ["network", "Network"],
              ["file", "File"],
              ["integrity", "Integrity"],
              ["detection", "Detection"],
            ].map(
              ([value, label]) => (

                <button
                  key={value}
                  className={`filter-button ${
                    activeFilter ===
                    value
                      ? "active"
                      : ""
                  }`}
                  onClick={() =>
                    setActiveFilter(
                      value
                    )
                  }
                >
                  {label}
                </button>

              )
            )}

          </div>


          {/* SEARCH */}

          <div className="search-row">

            <input
              type="text"
              className="search-input"
              placeholder="Search events, processes, files, rules..."
              value={searchTerm}
              onChange={(event) =>
                setSearchTerm(
                  event.target.value
                )
              }
            />

          </div>


          {/* EVENT LIST */}

          <div className="event-list">

            {loading ? (

              <div className="empty-state">
                Loading EDR events...
              </div>

            ) : recentEvents.length ===
              0 ? (

              <div className="empty-state">
                No matching events found
              </div>

            ) : (

              recentEvents.map(
                (event) => {

                  const isExpanded =
                    expandedEventId ===
                    event.event_id;

                  return (

                    <div
                      className={`event-item ${
                        isExpanded
                          ? "expanded"
                          : ""
                      } ${
                        event.event_category ===
                        "detection"
                          ? "detection-event"
                          : ""
                      }`}
                      key={
                        event.event_id
                      }
                      onClick={() =>
                        setExpandedEventId(
                          isExpanded
                            ? null
                            : event.event_id
                        )
                      }
                    >

                      <div className="event-summary">

                        <div className="event-left">

                          <span
                            className={`event-type ${getEventClass(
                              event
                            )}`}
                          >
                            {event.event_type ||
                              "unknown"}
                          </span>

                          <strong>
                            {getEventTitle(
                              event
                            )}
                          </strong>

                        </div>


                        <div className="event-right">

                          <span
                            className={`severity-badge ${(
                              event.severity ||
                              "INFO"
                            ).toLowerCase()}`}
                          >
                            {event.severity ||
                              "INFO"}
                          </span>

                          <span className="event-time">
                            {event.timestamp ||
                              ""}
                          </span>

                          <span className="expand-icon">
                            {isExpanded
                              ? "▲"
                              : "▼"}
                          </span>

                        </div>

                      </div>


                      {isExpanded && (

                        <div className="event-details">

                          <div className="detail-grid">

                            <div className="detail-row">

                              <span>
                                Event ID
                              </span>

                              <code>
                                {
                                  event.event_id
                                }
                              </code>

                            </div>


                            <div className="detail-row">

                              <span>
                                Event Type
                              </span>

                              <strong>
                                {
                                  event.event_type ||
                                  "N/A"
                                }
                              </strong>

                            </div>


                            <div className="detail-row">

                              <span>
                                Category
                              </span>

                              <strong>
                                {
                                  event.event_category ||
                                  "N/A"
                                }
                              </strong>

                            </div>


                            <div className="detail-row">

                              <span>
                                Status
                              </span>

                              <strong>
                                {
                                  event.status ||
                                  "N/A"
                                }
                              </strong>

                            </div>


                            <div className="detail-row">

                              <span>
                                Source
                              </span>

                              <strong>
                                {
                                  event.source ||
                                  "N/A"
                                }
                              </strong>

                            </div>


                            <div className="detail-row">

                              <span>
                                Severity
                              </span>

                              <strong>
                                {
                                  event.severity ||
                                  "INFO"
                                }
                              </strong>

                            </div>


                            {event.rule && (

                              <div className="detail-row">

                                <span>
                                  Detection Rule
                                </span>

                                <strong>
                                  {event.rule}
                                </strong>

                              </div>

                            )}


                            {event.detection && (

                              <div className="detail-row">

                                <span>
                                  Detection
                                </span>

                                <strong>
                                  {
                                    event.detection
                                  }
                                </strong>

                              </div>

                            )}

                          </div>


                          <div className="raw-details">

                            <div className="raw-details-title">
                              Event Details
                            </div>

                            <pre>
                              {formatValue(
                                event.details
                              )}
                            </pre>

                          </div>

                        </div>

                      )}

                    </div>

                  );
                }
              )

            )}

          </div>

        </div>


        {/* =========================
            MITRE ATT&CK
            ========================= */}

        <div className="panel">

          <div className="panel-header">

            <h2>
              MITRE ATT&amp;CK
            </h2>

            <span>
              Mapped Techniques
            </span>

          </div>

          <div className="mitre-list">

            {events
              .filter(
                (event) =>
                  event.details?.mitre
              )
              .slice()
              .reverse()
              .map((event) => {

                const mitre =
                  event.details.mitre;

                return (

                  <div
                    className="mitre-item"
                    key={
                      event.event_id
                    }
                  >

                    <span className="mitre-id">
                      {
                        mitre.technique_id
                      }
                    </span>

                    <strong>
                      {
                        mitre.technique
                      }
                    </strong>

                    <span className="mitre-tactic">
                      {mitre.tactic}
                    </span>

                  </div>

                );

              })}

            {events.filter(
              (event) =>
                event.details?.mitre
            ).length === 0 && (

              <div className="empty-state">
                No MITRE mappings
              </div>

            )}

          </div>

        </div>


        {/* =========================
            SYSTEM STATUS
            ========================= */}

        <div className="panel">

          <div className="panel-header">

            <h2>
              System Status
            </h2>

            <span>
              Monitoring
            </span>

          </div>

          <div className="system-status-list">

            <div className="system-status-item">

              <span>
                Process Monitor
              </span>

              <strong className="healthy">
                Active
              </strong>

            </div>


            <div className="system-status-item">

              <span>
                File Monitor
              </span>

              <strong className="healthy">
                Active
              </strong>

            </div>


            <div className="system-status-item">

              <span>
                File Integrity
              </span>

              <strong className="healthy">
                Active
              </strong>

            </div>


            <div className="system-status-item">

              <span>
                Network Monitor
              </span>

              <strong className="healthy">
                Active
              </strong>

            </div>


            <div className="system-status-item">

              <span>
                Detection Engine
              </span>

              <strong className="healthy">
                Active
              </strong>

            </div>


            <div className="system-status-item">

              <span>
                API
              </span>

              <strong
                className={
                  apiOnline
                    ? "healthy"
                    : "danger-text"
                }
              >
                {apiOnline
                  ? "Online"
                  : "Offline"}
              </strong>

            </div>

          </div>

        </div>

      </section>

    </div>
  );
}

export default App;