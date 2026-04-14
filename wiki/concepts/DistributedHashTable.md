---
title: "Distributed Hash Table (DHT)"
type: concept
tags: [distributed-systems, p2p, storage]
sources: [system-design-primer]
last_updated: 2026-04-14
---

## Summary
A decentralized distributed system that provides a lookup service similar to a hash table, where key-value pairs are stored across a peer-to-peer network. Used by Dropbox, BitTorrent, and others for peer-based file synchronization.

## Key Properties
- Decentralized — no single point of control
- Scalable — O(log n) lookup complexity
- Fault-tolerant — nodes can join/leave dynamically

## Connections
- [[DistributedSystems]] — underlying theory
- [[Dropbox]] — uses DHT for peer sync
