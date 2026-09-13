import { useEffect, useState } from "react";
import "./App.css";


function getSeverityClass(severity) {

  if (severity === "HIGH") {
    return "severity-high";
  }

  if (severity === "MEDIUM") {
    return "severity-medium";
  }

  return "severity-info";
}


function getEventTitle(event) {

  if (event.event_type === "process_created") {
    return "PROCESS CREATED";
  }

  if (event.event_type === "network_connection") {
    return "NETWORK CONNECTION";
  }

  if (event.event_type === "file_created") {
    return "FILE CREATED";
  }

  if (event.event_type === "file_modified") {
    return "FILE MODIFIED";
  }

  if (event.event_type === "file_deleted") {
    return "FILE DELETED";
  }

  if (event.event_type === "file_integrity_changed") {
    return "FILE INTEGRITY CHANGED";
  }

  if (event.event_type === "file_integrity_deleted") {
    return "FILE INTEGRITY DELETED";
  }

  if (event.event_type === "detection") {
    return event.rule || "DETECTION";
  }

  return event.event_type || "EVENT";
}


function getEventDetails(event) {

  const details = event.details || {};


  // ==========================================================
  // Process Event
  // ==========================================================

  if (event.event_type === "process_created") {

    return (
      <>
        <p>
          {details.process || "Unknown process"}
          {" · "}
          PID {details.pid ?? "N/A"}
        </p>

        {details.parent_pid !== undefined && (
          <p>
            Parent PID: {details.parent_pid}
          </p>
        )}
      </>
    );
  }


  // ==========================================================
  // Network Event
  // ==========================================================

  if (event.event_type === "network_connection") {

    const localAddress =
      details.local_ip && details.local_port
        ? `${details.local_ip}:${details.local_port}`
        : "Unknown";

    const remoteAddress =
      details.remote_ip && details.remote_port
        ? `${details.remote_ip}:${details.remote_port}`
        : "Unknown";

    return (
      <>
        <p>
          {details.process || "Unknown process"}
          {" · "}
          PID {details.pid ?? "N/A"}
        </p>

        <p>
          {localAddress}
          {" → "}
          {remoteAddress}
        </p>

        <p>
          Status: {details.status || "Unknown"}
        </p>
      </>
    );
  }


  // ==========================================================
  // File Events
  // ==========================================================

  if (
    event.event_type === "file_created" ||
    event.event_type === "file_modified" ||
    event.event_type === "file_deleted"
  ) {

    return (
      <>
        <p>
          {details.file_name || "Unknown file"}
        </p>

        <p>
          {details.path || "Unknown path"}
        </p>
      </>
    );
  }


  // ==========================================================
  // File Integrity Events
  // ==========================================================

  if (
    event.event_type === "file_integrity_changed" ||
    event.event_type === "file_integrity_deleted"
  ) {

    return (
      <>
        <p>
          {details.file_name || "Unknown file"}
        </p>

        {details.old_hash && (
          <p>
            Old SHA-256: {details.old_hash}
          </p>
        )}

        {details.new_hash && (
          <p>
            New SHA-256: {details.new_hash}
          </p>
        )}
      </>
    );
  }


  // ==========================================================
  // Detection
  // ==========================================================

  if (event.event_type === "detection") {

    return (
      <>
        <p>
          {event.detection || "Detection requires investigation"}
        </p>

        {details.evidence?.process && (
          <p>
            Process: {details.evidence.process}
          </p>
        )}
      </>
    );
  }


  return (
    <p>
      {event.source || "EDR telemetry"}
    </p>
  );
}


function getMixedRecentEvents(events) {

  const selected = [];

  const seenTypes = new Set();

  // ----------------------------------------------------------
  // First pass:
  // Pick recent events while preferring different types.
  // ----------------------------------------------------------

  for (
    let index = events.length - 1;
    index >= 0 && selected.length < 8;
    index--
  ) {

    const event = events[index];

    const eventType =
      event.event_type || "unknown";

    if (!seenTypes.has(eventType)) {

      selected.push(event);

      seenTypes.add(eventType);
    }
  }


  // ----------------------------------------------------------
  // Second pass:
  // Fill remaining slots with recent events.
  // ----------------------------------------------------------

  if (selected.length < 8) {

    for (
      let index = events.length - 1;
      index >= 0 && selected.length < 8;
      index--
    ) {

      const event = events[index];

      if (!selected.includes(event)) {

        selected.push(event);
      }
    }
  }


  return selected;
}


function App() {

  const [events, setEvents] = useState([]);
  const [incidents, setIncidents] = useState([]);


  // ==========================================================
  // Load EDR Data
  // ==========================================================

  useEffect(() => {

    const loadData = () => {

      fetch("http://localhost:8000/api/events")
        .then((response) => response.json())
        .then((data) => {

          setEvents(data);

        })
        .catch((error) => {

          console.error(
            "Failed to load events:",
            error
          );

        });


      fetch("http://localhost:8000/api/incidents")
        .then((response) => response.json())
        .then((data) => {

          setIncidents(data);

        })
        .catch((error) => {

          console.error(
            "Failed to load incidents:",
            error
          );

        });

    };


    // Load immediately
    loadData();


    // Refresh every 2 seconds
    const interval = setInterval(
      loadData,
      2000
    );


    return () => {

      clearInterval(interval);

    };

  }, []);


  // ==========================================================
  // Detection Events
  // ==========================================================

  const alerts = events.filter(
    (event) =>
      event.event_category === "detection"
  );


  // ==========================================================
  // High Severity Alerts
  // ==========================================================

  const highSeverity = events.filter(
    (event) =>
      event.severity === "HIGH" &&
      event.event_category === "detection"
  );


  // ==========================================================
  // MITRE Mapped Alerts
  // ==========================================================

  const mitreAlerts = alerts.filter(
    (alert) =>
      alert.details?.mitre
  );


  // ==========================================================
  // Mixed Recent Activity
  // ==========================================================

  const recentEvents =
    getMixedRecentEvents(events);


  return (

    <div className="dashboard">


      {/* ======================================================
          Header
          ====================================================== */}

      <header className="header">

        <div>

          <h1>
            Mini EDR
          </h1>

          <p>
            Endpoint Detection & Response Dashboard
          </p>

        </div>


        <div className="status">

          <span className="status-dot"></span>

          EDR Active

        </div>

      </header>



      {/* ======================================================
          Statistics
          ====================================================== */}

      <section className="stats">


        <div className="stat-card">

          <span>
            Total Events
          </span>

          <strong>
            {events.length}
          </strong>

        </div>


        <div className="stat-card">

          <span>
            Total Alerts
          </span>

          <strong>
            {alerts.length}
          </strong>

        </div>


        <div className="stat-card">

          <span>
            High Severity
          </span>

          <strong>
            {highSeverity.length}
          </strong>

        </div>


        <div className="stat-card">

          <span>
            Incidents
          </span>

          <strong>
            {incidents.length}
          </strong>

        </div>


      </section>



      {/* ======================================================
          Main Dashboard
          ====================================================== */}

      <main className="main-grid">


        {/* ====================================================
            Recent Alerts
            ==================================================== */}

        <section className="panel">

          <div className="panel-header">

            <h2>
              Recent Alerts
            </h2>

            <span>
              Detection Engine
            </span>

          </div>


          {alerts.length === 0 ? (

            <div className="empty-state">

              <p>
                No alerts available
              </p>

              <span>
                Detection events will appear here.
              </span>

            </div>

          ) : (

            <div className="event-list">

              {alerts
                .slice(-5)
                .reverse()
                .map((alert) => (

                  <div
                    className="event"
                    key={alert.event_id}
                  >

                    <div
                      className={`event-indicator ${getSeverityClass(
                        alert.severity
                      )}`}
                    ></div>


                    <div>

                      <strong>
                        {alert.rule}
                      </strong>

                      <p>
                        {alert.detection}
                      </p>

                    </div>

                  </div>

                ))}

            </div>

          )}

        </section>



        {/* ====================================================
            Incidents
            ==================================================== */}

        <section className="panel">

          <div className="panel-header">

            <h2>
              Incidents
            </h2>

            <span>
              Incident Manager
            </span>

          </div>


          {incidents.length === 0 ? (

            <div className="empty-state">

              <p>
                No incidents available
              </p>

              <span>
                Created incidents will appear here.
              </span>

            </div>

          ) : (

            <div className="event-list">

              {incidents
                .slice(-5)
                .reverse()
                .map((incident) => (

                  <div
                    className="event"
                    key={incident.incident_id}
                  >

                    <div
                      className={`event-indicator ${getSeverityClass(
                        incident.severity
                      )}`}
                    ></div>


                    <div>

                      <strong>
                        {incident.incident_id}
                      </strong>

                      <p>
                        {incident.rule} ·{" "}
                        {incident.severity}
                      </p>

                    </div>

                  </div>

                ))}

            </div>

          )}

        </section>



        {/* ====================================================
            Recent Event Activity
            ==================================================== */}

        <section className="panel wide">

          <div className="panel-header">

            <h2>
              Recent Event Activity
            </h2>

            <span>
              EDR Telemetry
            </span>

          </div>


          {recentEvents.length === 0 ? (

            <div className="empty-state">

              <p>
                No events available
              </p>

              <span>
                EDR telemetry will appear here.
              </span>

            </div>

          ) : (

            <div className="event-list">

              {recentEvents.map((event) => (

                <div
                  className="event"
                  key={event.event_id}
                >

                  <div
                    className={`event-indicator ${getSeverityClass(
                      event.severity
                    )}`}
                  ></div>


                  <div className="event-content">

                    <strong>
                      {getEventTitle(event)}
                    </strong>

                    {getEventDetails(event)}

                  </div>

                </div>

              ))}

            </div>

          )}

        </section>



        {/* ====================================================
            MITRE ATT&CK
            ==================================================== */}

        <section className="panel">

          <div className="panel-header">

            <h2>
              MITRE ATT&CK
            </h2>

            <span>
              Mapped Techniques
            </span>

          </div>


          {mitreAlerts.length === 0 ? (

            <div className="empty-state">

              <p>
                No techniques detected
              </p>

              <span>
                MITRE mappings will appear here.
              </span>

            </div>

          ) : (

            <div className="event-list">

              {mitreAlerts
                .slice(-5)
                .reverse()
                .map((alert) => {

                  const mitre =
                    alert.details.mitre;


                  return (

                    <div
                      className="event"
                      key={alert.event_id}
                    >

                      <div
                        className={`event-indicator ${getSeverityClass(
                          alert.severity
                        )}`}
                      ></div>


                      <div>

                        <strong>
                          {mitre.technique_id}
                        </strong>

                        <p>
                          {mitre.technique} ·{" "}
                          {mitre.tactic}
                        </p>

                      </div>

                    </div>

                  );

                })}

            </div>

          )}

        </section>



        {/* ====================================================
            System Status
            ==================================================== */}

        <section className="panel">

          <div className="panel-header">

            <h2>
              System Status
            </h2>

            <span>
              Monitoring
            </span>

          </div>


          <div className="system-status">


            <div>

              <span>
                Process Monitor
              </span>

              <strong>
                Active
              </strong>

            </div>


            <div>

              <span>
                File Monitor
              </span>

              <strong>
                Active
              </strong>

            </div>


            <div>

              <span>
                FIM
              </span>

              <strong>
                Active
              </strong>

            </div>


            <div>

              <span>
                Network Monitor
              </span>

              <strong>
                Active
              </strong>

            </div>


          </div>

        </section>


      </main>

    </div>

  );
}


export default App;