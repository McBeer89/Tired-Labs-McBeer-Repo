# Structuring Cyber Threat Intelligence Assessments

*Key points from Robert M. Lee's blog post, January 15, 2022*  
*Source: [robertmlee.org](https://www.robertmlee.org/structuring-cyber-threat-intelligence-assessments-musings-and-recommendations/)*

---

## The First Rule of CTI

If you are being an honest broker, and you are satisfying the requirement of your customer, then everyone else's opinion about how you got there is irrelevant. Intelligence serves the consumer's requirement — it does not exist for the intelligence team's purposes.

**Trust is everything.** CTI analysts operate in a world of trust because much of what they do looks like magic to those not in the field. If you betray that trust — especially on topics people aren't well-versed in and therefore need to rely on trust more — you're done.

---

## Being Precise in Word Usage

Sherman Kent's 1964 CIA paper *"Words of Estimative Probability"* established the necessity of being measured and consistent in language. The key isn't which standard you pick — it's that you pick one, define it, make it transparent, and apply it consistently.

**Recommendations:**

- Create a style guide for your team defining the words you do and don't use
- Tie words to numbers so consumers understand how they relate to each other
- Define words you explicitly avoid (e.g., Lee cannot stand the word "believe" in intelligence assessments — belief is for religion, not intelligence)
- Reduce barriers and friction between the consumer and the intelligence. Write briefly. Remove ambiguity.

**The Pepsi Challenge test:** Remove logos, branding, and color from your intelligence product. Place it randomly next to other teams' reports. Your consumer should be able to identify which one is yours based on language consistency, report structure, where assessments are placed, and where actions are suggested.

---

## Intelligence Assessments vs. Factual Statements

**Factual statements** are provable yes/no answers. "Was this malware on this system?" can be proven. There should be no intelligence assessment for factual statements — even if the fact is part of the threat intelligence.

**Intelligence assessments** go one step beyond the evidence. They are the analysis and synthesis of data and information to create new insights. Assessments require an analytical leap.

**Wrong:** "We assess with moderate confidence the malware is on that system." (That's provable — go check.)

**Right:** "We assess with low confidence, given the presence of the malware on the system, that our company is a target of their operation." (Whether the adversary intended to target you vs. you being a random victim requires an analytical leap.)

---

## Confidence Levels

Most organizations use three levels. Lee recommends against adding mid-points (Low-Moderate, Moderate-High) as they confuse consumers more than they help.

### Low Confidence

A hypothesis supported by available information. Likely single-sourced. Known collection and information gaps exist. This is a good assessment that is supported — it may not be finished intelligence and may not be appropriate as the sole factor in a decision.

### Moderate Confidence

Supported by multiple pieces of available information. Collection gaps significantly reduced. May still be single-sourced but with multiple data points supporting the hypothesis. Gaps have been accounted for even if not all addressed.

### High Confidence

Supported by a predominant amount of available data and information across multiple sources. Collection gaps all but eliminated. Almost never single-sourced. Even if a collection gap exists that can't be filled, it's all but certain not to change the outcome.

---

## Key Clarifications on Confidence

**"Single-sourced" refers to where the information comes from.** Operating only on netflow or only on malware repositories like VirusTotal is unlikely to produce a high confidence assessment from any one of those alone. Commercial netflow access + malware repositories + third-party shared information together could reach high confidence.

**Collection/information gaps** are anywhere there's useful data you don't have access to. Missing the initial infection vector is a gap. Not having access to the C2 server is a gap. You must think through as many gaps as possible and what they might mean to the assessment. Some gaps you can solve; some you cannot.

**For attribution specifically,** Lee holds a higher standard than what he sees in some private sector reporting. "High confidence" for attribution thrown out based solely on incident response data or malware repositories is insufficient — you need much more than that, ideally including non-intrusion data.

---

## Structure of an Assessment

Assessments should follow a consistent, repeatable pattern:

### **Confidence + Analysis + Evidence + Sources**

**Example:**

> "We assess with **moderate confidence** that ELECTRUM is targeting the Ukrainian electric sector **based on** intrusions observed at the Kyiv electric transmission substation by our incident response team **as well as** publicly available data from the Ukrainian SSU."

The depth of analysis, evidence, and sources varies entirely based on what the consumer needs.

---

## Low Confidence Assessments Are Good Assessments

This is one of Lee's strongest points. Teams often make the mistake of trying to make everything Moderate or High confidence. This is wrong.

**The inverted pyramid:** If you looked at all assessments a team produces over a given period (quarterly or annually), the distribution should look like:

- **40–60%** — Low Confidence
- **20–30%** — Moderate Confidence
- **10–20%** — High Confidence

The difference between Low and High often comes down to **time and resources**, not analytical skill. If you only release Moderate and High, you're creating unnecessary barriers between the consumer and intelligence they could act on.

**If your boss only listens to High Confidence assessments:** Have a conversation. Pull historical data on your assessments vs. decisions made. Showcase that Low Confidence assessments have a role. You serve at the request of the consumers, but sometimes serving them means correcting them.

**Not everything needs to be an assessment.** It's fine to say: "We haven't assessed the situation yet, but here is my analytical judgment based on my experience and the available information."

**Being transparent with consumers empowers better decisions.** If they need higher confidence: "If we had X more time and Y more resources, we likely could raise the confidence level or find an alternative assessment."

---

## Recommended Resources

Lee links to five talks that form a CTI tradecraft curriculum. All are available on YouTube via the SANS DFIR channel:

1. **Katie Nickels** — *The Cycle of Cyber Threat Intelligence*  
   Condenses the FOR578 material into an hour-long overview of the CTI intelligence cycle.

2. **Lenny Zeltser** — *Hack the Reader: Writing Effective Threat Reports*  
   Covers formatting, structure, and reducing friction for consumers.

3. **Christian Paredes** — *Pen-to-Paper and the Finished Report*  
   A master class on translating tough questions into usable intelligence reports.

4. **Selena Larson** — *Threat Intel for Everyone: Writing Like a Journalist to Produce Clear, Concise Reports*  
   Lee recommends CTI teams consider hiring journalists — this talk demonstrates why.

5. **Michael Rea** — *I Can Haz Requirements? Requirements and CTI Program Success*  
   Everything ties to the requirement. Intelligence does not exist for intelligence's purposes. No one cares how smart you are or how much you learned — they care about information that meets their requirement so they can achieve their outcomes.

---

## Key Takeaways (Summary)

- Intelligence serves the consumer's requirement, not the analyst's curiosity
- Trust is the foundation — dishonesty (including FUD and pew-pew maps) destroys it
- Be precise and consistent in language — create a style guide, define your terms
- Factual statements don't get assessments; assessments go one step beyond evidence
- Use three confidence levels: Low, Moderate, High — define them, stick to them
- Structure every assessment as: Confidence + Analysis + Evidence + Sources
- Low confidence is a valid, useful assessment — don't hoard intelligence waiting for High
- The inverted pyramid (40-60% Low, 20-30% Moderate, 10-20% High) is normal and healthy
- Collection gaps must be identified and considered — they're intelligence about your intelligence
- Train your consumers to use all confidence levels, not just High
- Transparency with consumers about what would raise confidence empowers better decisions

---

*Robert M. Lee is the CEO of Dragos, a SANS Fellow, and co-author of SANS FOR578: Cyber Threat Intelligence. This post accompanied his PancakesCon 3 talk "Structuring Intelligence Assessments and Gin Cocktails" (January 16, 2022).*
