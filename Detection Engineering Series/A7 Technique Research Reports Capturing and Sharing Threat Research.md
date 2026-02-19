# Technique Research Reports: Capturing and Sharing Threat Research

**Author:** VanVleet  
**Published:** November 14, 2025  
**Reading Time:** 8 min read  
**Part of:** [Threat Detection Engineering: The Series](https://medium.com/@vanvleet/threat-detection-engineering-the-series-7fe818fdfe62)

![VanVleet Profile](https://miro.medium.com/v2/resize:fill:64:64/1*dmbNkD5D-u45r44go_cf0g.png)

---

In my article on [Technique Analysis and Modeling](https://medium.com/@vanvleet/technique-analysis-and-modeling-ffef1f0a595a), I talked about the need to document the results of your research. In this article, I'll share details about why and how to capture and share the output of technique analysis and modeling in a Technique Research Report (TRR). I'm also announcing a [public repository of TRRs](http://library.tired-labs.org) to enable the industry to share good technique analysis! Details on that at the end.

## The Detection Engineering Process

Before we get into the details of TRRs, let's first explore what we want to accomplish.

When creating a detection, a detection engineer (DE) will (hopefully!) follow a process similar to this:

1. **Research the technique** — some work must be done to understand the attack technique that will be detected. Ideally, this is robust and identifies all the procedures, but at a minimum there should be some effort to understand what the technique looks like.
2. **Identify possible telemetry** — determine what potential telemetry sources are available, so the DE knows what options they have to work with.
3. **Select a log source** — a log source(s) will be selected as the best option for detecting the technique in the target environment.
4. **Build the detection query** — write the query logic to actually implement the detection in a specific SIEM. The query also needs to be adapted to the target environment to minimize false positives.

Looking at these steps, some of them are universally applicable (those that involve understanding and identifying the technique) and some are environment specific (those that involve specific logs sources, SIEMs, and environment noise and tuning).

<!-- Image: Diagram showing detection engineering process steps with "Research Technique" and "Identify Telemetry" marked as universally applicable, while "Select Log Source" and "Build Detection Query" marked as environment specific -->

Identifying telemetry splits in the middle because some telemetry is commonly available (Windows event logs, for example), while some is environment specific (your particular EDR).

(As an aside, the universally applicable sections are generally those doing [identification](https://medium.com/@vanvleet/identifying-and-classifying-attack-techniques-002c0c4cd595), while the environment specific ones are doing [classification](https://medium.com/@vanvleet/identifying-and-classifying-attack-techniques-002c0c4cd595). This is unsurprising because classification is inherently environment specific.)

## Lossy and Lossless Information Capture

Let's take a quick side track. I'm going to borrow a concept from compression algorithms: lossy and lossless compression. Lossy compression is when you store information in a way that some of it is irrecoverably lost, while lossless compression keeps all of the information but attempts to pack it in as tightly as possible. We're all really familiar with this concept when dealing with pictures and videos. At some point, we all realize that we don't REALLY need to keep that 50MB, 200MP picture of us doing something stupid because we're unlikely to ever print a wall-sized poster of it. A lossy 3MB version is enough to keep the memory alive.

<!-- Image: Photo showing "Me, doing something stupid. But AWESOME." - appears to be someone in an unusual position or doing an athletic feat -->

The effort of capturing threat research has parallels. A technical write-up of an attack technique captures a lot of the information (lossless), while a detection query captures very little (lossy). Part of that is because a published detection, from a practical standpoint, can't come with 5 pages of documentation, including graphics and screen captures! The other part is that the act of creating a detection query involves environment specific decisions: selecting the best telemetry source available in that environment, determining which procedures actually apply there (and which are covered by other defensive layers), what noise to tune out (or not), what query capabilities the SIEM can support (or the given detection engineer was able to implement), etc. From the point where we take the universally applicable information and start to make decisions on a specific detection implementation, we begin losing some information. **The decisions that are best for one environment may NOT be the best for another, but the decisions made and details that informed them are not captured in the detection.** This information is lost. As a result, detection queries are a poor vehicle to capture and convey information about attack techniques!

## Measuring the Gap

Despite being a lossy vehicle, we share detection queries in the InfoSec industry all the time. There are numerous public repos and a dozen vendors offering thousands of pre-built detection queries for nearly every technique on the ATT&CK matrix. So here's the rub: when someone gets one (or thousands) of detection queries, they have to make a decision. Do they do the technique research to understand how the detections — and the procedures they are purported to detect — apply to their environment? Or do they just deploy them?

I like to compare this to the process of building a wall. When you're building a wall (imagine your favorite war strategy game here), you need to make an assessment of the gap that it's intended to block. How big is it, what shape is it, is actually a gap or just an alcove? Building without measuring the gap can result in a wall that gives the impression of safety but offers little real protection!

<!-- Image: Screenshot from CodeCombat.org game showing a poorly placed wall that doesn't properly block a gap -->

Source: CodeCombat.org, MY favorite war strategy game!

It looks ridiculous in the game, but I'd wager we have an awful lot of unmeasured detection walls in real life!

But detections aren't the only way we share technique research. There are many technique write-ups that have been published, but they take some time to sort. Some are excellent: thorough, accurate, and well presented. Others are boilerplate (and I swear half of them are AI-generated). And some are downright inaccurate! What's most problematic, though, is that the majority of them only cover a single, well-known procedure. The end result is that it can take quite a bit of time to do thorough technique analysis and modeling, even for well-documented procedures. If you're too hasty about it, you'll have an incomplete understanding of the technique, resulting in an incomplete detection strategy and a poorly measured wall.

## Technique Research Reports — Lossless Capture and Sharing

Coming back full circle, the portion of our technique analysis that is most useful to capture and share is the universal part.

<!-- Image: Diagram highlighting "Research Technique" and "Identify Telemetry" as the universally applicable portions worth capturing in TRRs -->

This is the purpose of a Technique Research Report (TRR). A TRR documents the distinct procedures that implement a technique, including the background and technical information necessary to understand how those procedures work. **TRRs provide the context, information, and potential telemetry needed to create a robust detection strategy tailored to your specific environment.**

Let's take the Kerberoasting detection data model we created in the [Detection Engineering Dispatch podcast](https://www.youtube.com/watch?v=5DAQkvOyqME&list=PLeaA8CQiZrWyodUEdNL2yBA4dM5TTBkrI&index=15):

<!-- Image: DDM for Kerberoasting (T1558.003) showing complete operation flow and telemetry sources -->

A [TRR on Kerberoasting](https://github.com/tired-labs/techniques/blob/main/reports/trr0018/ad/README.md) will contain this DDM, a list of the distinct procedures we've identified, and all the background information needed to understand them.

With this information, a detection engineer should have no difficulty determining which of the procedures work in their environment and what telemetry (either from the DDM or unique to their environment) they have available to build their detection strategy. Measuring the gap becomes easy, all that's left is to build the wall.

## The TRR Repository

To make it easier to share thorough attack technique research, I have created a public [TRR Library](http://library.tired-labs.org) on GitHub that the entire InfoSec industry can use and contribute to. I've already got some of my own work in there, and would love for you to contribute your work, too! With time, I'm hoping this can become a real force multiplier for the InfoSec community: a place to find and share high quality technique analysis and modeling that can speed up your efforts to deploy thorough detections.

Do you have some great technique analysis you'd like to share? Want a future employer to see what you can really do? Pick an attack technique, do some mind-blowing modeling and analysis, document it in a TRR, and submit a PR to have it included in the Library! Cred for you, excellent research for all of us. We all win! :) Here's the [contribution guide](https://github.com/tired-labs/techniques/blob/main/docs/CONTRIBUTING.md).

## TRR Format

While any format would work, I'll share the format the TRR library is using. For more details, the Library has a detailed [TRR Guide](https://github.com/tired-labs/techniques/blob/main/docs/TECHNIQUE-RESEARCH-REPORT.md).

### TRR Title

### **Categorization Section**

This section captures some of the metadata for the technique: the platforms it applies to, the MITRE technique number, etc.

* **Technique ID —** This is a unique ID to identify the technique in the Library. It's assigned when the TRR is accepted for publication.
* **External IDs —** The ID for the technique on all relevant threat matrices (doesn't have to just be ATT&CK)
* **Tactic —** The tactic(s) that this technique falls under.
* **Platforms** **—** The platforms that are covered in this TRR. Do not list platforms where the technique applies but will not be addressed in this TRR, those should be listed in the TRR that covers them.

**Scope Statement (optional)**

TRRs are focused on a single, specific attack technique or sub-technique for a specific platform. This is an optional statement of the scope of the TRR, like how it maps to techniques on other matrices and any rationale for the choice on scope.

### **Technique Overview Section**

This section is the executive summary of the attack technique.

### **Technical Background Section**

This section contains the real substance of the TRR. It should capture all the key technical details and background needed to understand how the technique works. The rule of thumb is to ensure that the reader doesn't need to go anywhere else for the details needed to understand the technique. Links can be provided to further details, but the key details should be included here. The structure of this section is not rigid, the author has discretion to determine the best way to present the information.

### **Procedures Section**

This section begins with the below table identifying each unique procedure that implements the technique:

<!-- Image: Example table showing procedure listing with columns for Procedure ID, Name, and Description -->

Following the table will be individual sections for each procedure, which will contain a summary of the procedure, a detection data model (DDM), and any additional technical details or background that are specific to the procedure (details relevant to all procedures should be in the Technical Background section above). It is possible that no additional detail is required for a procedure, in this case the section will simply contain a summary of the procedure and a DDM. This is where you might add ideas for how a procedure could be identified, any details about the telemetry identified in the DDM (specific field values, for example), and other useful but not environment-specific information about the procedure.

**Procedure #1 Details**

<Image of DDM>

Details of the procedure.

**Procedure #2 Details**

<Image of DDM>

Details of the procedure.

### **References Section**

This section is used to capture reference documents used in the TRR, good explainers, and other resources that would help someone dive deeper into the technique or platform.

## Conclusion

Thanks for reading today! Hopefully I've offered a compelling reason for why we as a detection engineering community should be doing thorough technique analysis and modeling and sharing our work with one another. I'll see you on GitHub!

---

**Tags:** Detection Engineering, Information Sharing, Cybersecurity, Threat Research