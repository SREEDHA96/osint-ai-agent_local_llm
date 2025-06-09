# backend/memory.py

import time
from collections import defaultdict
from typing import Dict, List

class OSINTMemory:
    def __init__(self):
        self.source_scores: Dict[str, float] = defaultdict(lambda: 0.5)  # Default credibility
        self.entity_graph: Dict[str, Dict[str, float]] = defaultdict(dict)
        self.timeline: List[Dict] = []
        self.provenance_log: List[Dict] = []

    def update_source_score(self, source: str, credibility: float):
        self.source_scores[source] = round(min(max(credibility, 0), 1), 2)

    def add_entity_relationship(self, entity_a: str, entity_b: str, confidence: float):
        self.entity_graph[entity_a][entity_b] = round(min(max(confidence, 0), 1), 2)

    def add_event_to_timeline(self, event: str, date: str, details: str):
        self.timeline.append({"event": event, "date": date, "details": details})

    def log_provenance(self, article_title: str, source: str, timestamp: float):
        self.provenance_log.append({
            "article": article_title,
            "source": source,
            "timestamp": timestamp
        })

    def get_summary(self):
        return {
            "source_scores": self.source_scores,
            "entity_graph": self.entity_graph,
            "timeline": self.timeline,
            "provenance_log": self.provenance_log
        }

# Singleton memory instance
memory = OSINTMemory()
