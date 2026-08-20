============================================================
 NETWORK DEFENSE PLAN
============================================================

Prepared by:    Abhinav Sabu
Date:           August 20, 2026
Client:         Maya's Clothing Shop (small retail business)
Engagement:     Network Security Assessment and Remediation Plan


------------------------------------------------------------
 1. ASSESSMENT SUMMARY
------------------------------------------------------------

Maya's network is a single flat network with little or no
segmentation between payment systems, customer Wi-Fi, staff
devices, and IoT devices. The main risks are the lack of
segmentation, customer Wi-Fi sharing the payment environment,
outdated cameras, exposed Wi-Fi credentials, and default router
administrator credentials. The most urgent priority is to
separate payment systems from customer and IoT networks and
secure the router administration. Prioritised changes can
significantly reduce the attack surface and limit lateral
movement.


------------------------------------------------------------
 2. NETWORK INVENTORY
------------------------------------------------------------

Device / system          Category          Holds / does
Payment till x2          Payment           Processes card transactions
Security cameras x4      IoT               Security monitoring; outdated firmware
Back-office laptop       Data              Business/customer records and work
Maya's laptop            Personal/Business Personal + business activity
Staff phones x2          Staff             Connect to shop Wi-Fi
Smart speaker            IoT               Personal smart device on network
Network printer          Infrastructure    Shared printing
Customer Wi-Fi           Guest             Customer internet access; shares main network
ISP router               Infrastructure    Network access; default admin credentials


------------------------------------------------------------
 3. PRIORITISED RISKS
------------------------------------------------------------

CRITICAL
  [ ] Flat network: compromised devices may reach payment tills,
      laptops, cameras, and other systems. There are few barriers
      to lateral movement.
  [ ] Customer Wi-Fi shares the network with payment systems,
      allowing untrusted devices potential access to the business
      environment.
  [ ] Default router administrator credentials could allow an
      attacker who gains access to take control of network settings.

HIGH
  [ ] Shared Wi-Fi password is three years old and publicly
      displayed, making the credential exposed and difficult to control.
  [ ] No useful monitoring or logs: an attack could go unnoticed
      and investigation would be difficult.

MEDIUM
  [ ] Four never-updated IoT cameras may contain known
      vulnerabilities and are not properly isolated.
  [ ] Shared back-office laptop may contain customer/business
      data and provides poor individual accountability.
  [ ] Personal laptop is used for business activity, mixing
      personal and business use.

LOW
  [ ] Unmanaged smart speaker adds another IoT device and
      increases the attack surface.


------------------------------------------------------------
 4. RECOMMENDED FIXES
------------------------------------------------------------

  - SEGMENT the network into separate networks for payment
    systems, customer Wi-Fi, IoT/cameras, and staff/office devices.
    Block unnecessary communication between these networks.

  - ISOLATE customer Wi-Fi using a guest network with internet
    access only. Customer devices should not reach payment tills,
    staff devices, cameras, printers, or router administration.

  - CHANGE the router administrator password from the default to
    a strong, unique password and update router firmware.

  - SECURE Wi-Fi with WPA3 where supported, or WPA2 minimum.
    Replace the old password with a strong unique password and
    remove it from the public chalkboard.

  - UPDATE all four camera firmware versions. Replace cameras
    that are no longer supported.

  - ISOLATE cameras and other IoT devices on a dedicated IoT
    network with restricted access to business systems.

  - IMPROVE ACCESS CONTROL by giving staff individual accounts
    where possible and applying least privilege to business and
    customer data.

  - SEPARATE personal and business activity by using a dedicated
    business device for sensitive business operations where possible.

  - ENABLE basic router/network logging and review it regularly.
    Consider managed monitoring as the business grows.

  - REMOVE or isolate unnecessary devices such as the smart speaker.


------------------------------------------------------------
 5. PHASED ACTION PLAN
------------------------------------------------------------

DO FIRST (critical, highest leverage):
  [ ] Change default router administrator credentials
  [ ] Update router firmware
  [ ] Segment payment systems away from customer Wi-Fi
  [ ] Create a guest network that cannot access business systems
  [ ] Restrict router administration from untrusted networks

THIS WEEK:
  [ ] Replace the old Wi-Fi password with a strong unique password
  [ ] Enable WPA3 if supported, or WPA2 at minimum
  [ ] Remove the Wi-Fi password from the public chalkboard
  [ ] Separate IoT cameras onto their own network
  [ ] Update all four camera firmware versions
  [ ] Review access to the shared back-office laptop

THIS MONTH:
  [ ] Enable and review network/router logging
  [ ] Create individual staff accounts where practical
  [ ] Separate personal and business laptop usage
  [ ] Review the smart speaker and unnecessary IoT devices
  [ ] Identify unsupported devices that need replacement
  [ ] Maintain an up-to-date network inventory


------------------------------------------------------------
 6. HOW MAYA WILL KNOW IT WORKED
------------------------------------------------------------

  1. Customer devices can no longer reach the payment/till
     network, staff devices, cameras, or router administration.

  2. The router no longer uses default administrator credentials,
     Wi-Fi uses WPA3/WPA2, and the public Wi-Fi password has been
     replaced and removed from the chalkboard.

  3. The cameras are updated and isolated on their own network,
     while network logging is active and available for investigation.


============================================================
 END OF PLAN
============================================================
