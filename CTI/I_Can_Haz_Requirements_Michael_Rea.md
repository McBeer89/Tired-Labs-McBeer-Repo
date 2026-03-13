# I Can Haz Requirements? Intelligence Requirements and CTI Program Success

*Key points from Michael Rea's presentation at SANS CTI Summit*  
*Source: [youtube.com/watch?v=Aqo3IcVQs_M](https://www.youtube.com/watch?v=Aqo3IcVQs_M)*

---

## The Core Problem

CTI teams place heavy emphasis on collection, analysis, and the end deliverable — but devote very little to generating and managing intelligence requirements at the onset of the intelligence cycle. Without aligning analytic efforts to pre-existing requirements, the team diminishes its value to the organization.

> "We all have our little pet interests, our side projects, that we care deeply and passionate about. Sometimes they align with what we're working on in our nine-to-five capacity, but without that structured planning and requirements generation at the onset of the intelligence production cycle, you start licking an ice cream cone — and intelligence that doesn't meet a specified need only has so much value."

---

## Why You Need Requirements

Requirements help intelligence teams:

- **Answer critical questions** that consumers actually have about the threat environment
- **Scope the end deliverable** — what you're producing through your analytic efforts
- **Prioritize collection capabilities** — where you're postured to collect the data you need
- **Identify gaps in data sources** — if you're tasked to focus on something but your access to that data is limited, gap analysis helps mitigate visibility deficiencies
- **Get ahead of the adversary** — which is the entire point

Without the planning and requirements phase of the intelligence cycle, you cannot do the rest of the cycle effectively. It hinders collection prioritization, timely analysis, and getting finished intelligence to decision-makers when, how, and where they need it.

---

## Requirements Are a Team Sport

You do not make requirements alone. They require feedback from:

- **Senior executives** within the organization
- **Sister teams** in the network fight alongside you (SOC, IR, forensics)
- **The people you didn't know needed you** — in large organizations, people may not know your team exists. When in doubt, reach out. You'll be surprised how many previously unknown customers you have who want to work with you.

### Technical Consumers
- Red team / penetration testers
- Security operations center (SOC)
- Incident response / digital forensics
- Brand reputation (if the organization has that function)

### Business / Executive Consumers
- C-suite (CISO, CSO, CEO)
- Board of directors
- Business planning / strategic vision leadership
- Procurement

---

## What Makes a Good Intelligence Requirement

A good intelligence requirement has four characteristics:

### 1. Timeliness
Intelligence that is late is as good as ignorance. If you can't deliver the right intelligence in time to meet the decision-making cycle, you're not providing value.

### 2. One Decision Point
It asks one specific question. It focuses on one specific activity, event, or thing. Overly verbose, Frankenstein requirements that try to cover everything will get a puzzled look from your CSO.

### 3. Supports Action (Including Inaction)
Requirements support the decision-making process — blocking something, procuring something, changing a policy. But an equally valid decision is **inaction**: the conscious choice not to do something. That's a legitimate decision point that intelligence must consider and support.

### 4. Answerable
Start with the six basic questions: who, what, when, where, why, and how. Short, specific questions based on these starters drive clear, concise, and succinct intelligence requirements.

---

## Where to Start Generating Requirements

### Threat Modeling and Attack Surface Analysis
If you haven't done it, do it. It will help you derive immediately relevant, organization-specific intelligence requirements that guide analytic efforts.

### Industry Vertical Analysis
No industry has the same threat profile. Strip away the rest of the marketplace and look at what's specific to your vertical. The threat groups targeting industrial control systems or energy are not the same ones targeting retail commerce. Focus on what's industrially relevant.

### Supply Chain
The supply chain always introduces known or unknown risks. Identify potential weaknesses — organizationally, on the network, operationally — that could invite an attacker in. Gauge intelligence requirements around how external relationships (vendors, outsourcing, downstream suppliers) affect your threat profile.

### Geographic Analysis
Where you are in the world determines which threat groups you face. It doesn't make sense to focus exclusively on threat groups in one region if your organization operates in another. Let geography inform your requirements.

### Crown Jewel Analysis
Take stock of what you have that an adversary would want. This drives intelligence production around adversary motivations and intent, and puts network activity into context. Finance? They want your money. Legal? They want privileged information. Manufacturing? They want your intellectual property.

---

## The RFI Process: Handling Ad-Hoc Requests

It's 5:00 PM on a Friday. Something happens. You get 10 calls from leadership with their hair on fire: "What is this? Why didn't you tell me? What can I do?"

This is where the **Request for Information (RFI)** process comes in. RFIs help manage ad-hoc, drive-by taskers that aren't covered by pre-existing requirements.

### Without an RFI Process
You get inundated with requests. You're not sure how to meet them, when they're due, and you get sidetracked from your standing intelligence production.

### Working the RFI

**Work with the customer.** They may not have a conceptual frame for what intelligence is. They just know they have a thing that does a thing and you can answer the thing. Their initial request may not be clear. Start a conversation. Massage the request. Trim it down to the bare essentials to get to the root question.

**Manage expectations by asking:**

- **What explicitly do they need?** What is the key intelligence question?
- **When do they need it?** They may expect the answer five minutes ago, but establish what's realistic: "If I have six hours, I can deliver this. If I have a day, I can do this. If I have a week, I can give you this."
- **What format?** Email? PowerPoint? A phone call? Don't assume you know what the customer wants. Ask. There's nothing worse than spending effort on a product you think looks awesome, only to get an angry email in red font saying "I don't want this, make it more digestible."
- **What decision does it support?** This is harder in large organizations, but try to understand what the customer will do with the information. Get into the customer's head and look at the request from their point of view to shape the deliverable.

### Tracking RFIs

Simple tools work:

- **Excel spreadsheet** — columns for requester, subject, due date, status
- **Dedicated Outlook inbox** — track the lifecycle of inbound/outbound RFIs with a clear timeline
- **SharePoint workflows** — combine document storage with Outlook integration for some automation

The point isn't sophisticated tooling. The point is having any tracking at all so you can measure your own efficacy and not lose requests.

---

## Metrics: Using Requirements to Prove Value

Leadership loves metrics. Intelligence teams struggle to generate them. Requirements give you a way.

### How It Works

1. **Number your requirements** (IR-1 through IR-6, etc.)
2. **Tag every finished product** back to the specific requirement it answers
3. **Count production** per requirement — IR-1 has 20 products, IR-2 has 5, IR-5 has zero
4. **Show where production is strongest and weakest** — numerically, visibly
5. **Analyze the gaps** — if a requirement has zero products, the common reason is a collection or capability gap

### What This Gets You

- Proof of where the team is delivering value and where it's not
- Identification of deficiencies — not just internal capabilities, but larger organizational gaps
- Justification for procurement — "We can't answer this requirement because we don't have the data source. Here's what it would cost to close that gap."
- Expectation-setting — what the team is currently capable of producing, for whom, and how quickly

---

## Final Takeaways

**If your organization isn't doing any requirements management at all, start the conversation now.** You can't fix what you didn't do yesterday, but you can correct it today.

**Make it a team sport.** Get leadership on the same page. They may not fully understand how intelligence functions, but if you invite them into the process early, it gives them ownership and commitment to a successful program. Providing timely, cogent analysis repeatedly over time earns trust — and that trust drives the growth of the intelligence team.

**Practice what you preach.** CTI professionals extol the intelligence cycle but focus mostly on collection, analysis, and production while leaving requirements and feedback to the wayside. To gain credibility as a discipline, embody the full intelligence tradecraft — including the planning and requirements phase that makes everything else work.

---

*Michael Rea is a career intelligence professional with experience at NSA, US Cyber Command, United Health Group, and McAfee. This talk was presented at the SANS CTI Summit.*

---

## References

- **Michael Rea** — *I Can Haz Requirements? Requirements and CTI Program Success*, SANS CTI Summit. [youtube.com/watch?v=Aqo3IcVQs_M](https://www.youtube.com/watch?v=Aqo3IcVQs_M)
- **Robert M. Lee** — *Structuring Cyber Threat Intelligence Assessments*. Referenced by Rea; expands on confidence levels and assessment structure. [robertmlee.org](https://www.robertmlee.org/structuring-cyber-threat-intelligence-assessments-musings-and-recommendations/)
- **SANS FOR578: Cyber Threat Intelligence** — The intelligence cycle and planning/direction phase that Rea's talk reinforces. [sans.org](https://www.sans.org/cyber-security-courses/cyber-threat-intelligence)
- **Sherman Kent** — *Words of Estimative Probability* (1964, CIA). Referenced by Rea via Lee's work on precise language in intelligence assessments.
- **UK Joint Military Doctrine** — "Intelligence that is late is as good as ignorance." Cited by Rea on the timeliness requirement.
