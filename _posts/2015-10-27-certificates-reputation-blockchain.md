---
layout: post
title: Certificates, Reputation, and the Blockchain
comments: true
tags: blockchain, bitcoin, certificates, credentials, blockcerts
---

# Certificates, Reputation, and the Blockchain

(Crossposted to Medium > https://medium.com/mit-media-lab/certificates-reputation-and-the-blockchain-aee03622426f#.rgm5rdnwb)

Earlier this year, the MIT Media Lab started issuing digital certificates to groups of people in our broader community. We use certificates as a way to recognize contributions we value, or simply to signal membership in the Media Lab family. For example, in July we issued coins and certificates to all of the [Media Lab Director’s Fellows](https://www.media.mit.edu/people/?filter=directors-fellow). The coins are physical representations of [digital certificates](https://certs.media.mit.edu/8ca9cad234bdc2136532072e4a01b4898d45ef128d0cec499e76903787b9430d) (see below).

![Coin]({{site}}/images/ml-certificates.png)

## Designing an Open Platform for Digital Certificates

Certificates are signals of achievement or membership and some are more important than others. University degrees (a particular type of certificate) can help you get the job you want, or prevent you from getting it if you don’t have the right certificate. Our current, mostly analog system for managing certificates is slow, complicated, and unreliable. There are many advantages for creating a digital infrastructure for certificates, but the stakes are high since such a system could grow to represent our professional reputations. We need to be thoughtful about its design, and the type of institutions we trust to govern it.

## The Journeymen History of Certificates

When we lived in small tight-knit communities, people knew whom they could turn to when they needed an expert (and whom to avoid). However, as we started moving around more and our lives and networks grew, we needed to come up with portable ways to signal our expertise to new acquaintances. Some of these original systems are still in place. For example, in Germany many carpenters still do an [apprenticeship tour](https://en.wikipedia.org/wiki/Journeyman_years) that lasts no less than three years and one day. They carry a small book in which they collect stamps and references from the master carpenters with whom they work along the way. The carpenter’s traditional (and now hipster) outfit, the book of stamps they carry, and — if all goes well — the certificate of acceptance into the carpenter guild are proof that here is a man or woman you can trust to build your house.

![Wandergeselle](https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/Wandergeselle_02.JPG/640px-Wandergeselle_02.JPG)

“Wandergeselle 02” by Sigismund von Dobschütz — CC BY-SA 3.0 via Wikipedia Commons

Ideally we should be in charge of our own credentials, similar to the journeymen carpenters who carry around their books of stamps and references. But most of the time we have to rely on third parties, such as universities or employers to store, verify, and validate our credentials. Job seekers have to request official transcripts from their alma maters (and typically pay a small fee), and employers still need to call the university if they want to be sure that a transcript wasn’t faked. It’s a slow and complicated process, which is one reason why degree fraud is a real issue. (A few years back, even our very own MIT Admissions office realized that its [Dean didn’t actually have the undergraduate degree](http://www.nytimes.com/2007/04/27/us/27mit.html) that she had listed in her application). Making certificates transferable and more easily verifiable is one advantage of digital systems.

![Wanderbuch](https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Wanderbuch2.jpg/607px-Wanderbuch2.jpg)

*“Wanderbuch” by Magistrate der Königl. Freystadt Oedenburg im Königreiche Ungarn / Public Domain*

## An Open Platform for Reputation

The trail of credentials and achievements that we generate throughout our lives says something about who we are, and it can open doors that allow us to become who we want to be. Some credentials, such as university degrees, are more important than others. But at the end of the day, all of these credentials represent experiences that are part of our lives.

There are many advantages for recipients to have more control over the certificates they earn. Being in control doesn’t mean it would be easy to lie. Similar to the carpenter’s book of references, it should not be possible to just rip out a few pages without anyone noticing. But being in control means having a way to save credentials, to carry them around with us, and to share them with an employer if we chose to do so (without having to pay, or ask for the issuer’s permission or cooperation).

In order to make that happen we need an open platform for digital certificates and reputation. Using the blockchain and strong cryptography, it is now possible to create a certification infrastructure that puts us in control of the full record of our achievements and accomplishments. It will allow us to share a digital degree with an employer while giving the employer complete trust that the degree was in fact issued to the person presenting it.

This is exciting because it is not only a better way to deal with the way certificates work today, but it is also an opportunity to think about what certificates may look like in the future. A few years ago, I co-authored a [white paper](https://wiki.mozilla.org/images/b/b1/OpenBadges-Working-Paper_092011.pdf) with Mozilla on digital badges (just another name for certificates) in which we set out some of these core ideas. What was missing at the time was the technical infrastructure that would let us reliably store and manage the certificates. Enter the blockchain.

The blockchain is best known for its connection to the [cryptocurrency bitcoin](https://en.wikipedia.org/wiki/Bitcoin). But in essence it is a just a distributed ledger to record transactions. What makes it special is that it is durable, time-stamped, transparent, and decentralized. Those characteristics are equally useful for managing financial transactions, as for a system of reputation. In fact you can think of reputation as a type of currency for social capital, rather than financial capital.

## How It Works

Issuing a certificate is relatively simple: we create a digital file that contains some basic information such as the name of the recipient, the name of the issuer (MIT Media Lab), an issue date, etc. We then sign the contents of the certificate using a private key to which only the Media Lab has access, and append that signature to the certificate itself. Next we create a hash, which is a short string that can be used to verify that nobody has tampered with the content of the certificate. And finally we use our private key again to create a record on the Bitcoin blockchain that states we issued a certain certificate to a certain person on a certain date. Our system makes it possible to verify who a certificate was issued to, by whom, and validate the content of the certificate itself.

## What’s Next?

We will continue to develop our software tools and issue certificates to members of the Media Lab community. We will also start releasing software under an open source license so that others can review it, extend and improve our work, or just learn from it. And we are collaborating with MIT’s Digital Currency Initiative to explore some of the privacy implications and technical infrastructure questions.

In addition, we are actively looking for collaborators to build out a few example implementations outside the Media Lab. Areas in which digital certificates provide exciting opportunities include:
		Corporate/ enterprise training — Many large companies offer a myriad of training opportunities to their employees, but they lack systems to reliably track and store the results. Existing HR systems are often monolithic and don’t talk to other corporate databases, there are no consistent ways to compare skills, and accomplishments are not portable.
		Workforce development — There are millions of apprenticeship records and certificates, but no systems to manage them. This is especially an issue for the 36M adults in the US with low skills, who often lack other more recognized diplomas or degrees.

Interested in learning more? Get in touch with us at coins@media.mit.edu and follow our research updates at http://certificates.media.mit.edu.

Philipp Schmidt is Director of Learning Innovation at the MIT Media Lab. He works with a team of students, designers, and researchers to enhance the Media Lab’s learning culture and community, and liaises with member companies and other partners to promote creative learning outside the Media Lab.
