-- One row per vote on a set of three kit colors (token names, e.g. "pink-5").
-- voter is a random id the browser makes up and keeps; it ties a person's
-- votes together without saying who they are.
CREATE TABLE votes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ground TEXT NOT NULL,
  text TEXT NOT NULL,
  accent TEXT NOT NULL,
  liked INTEGER NOT NULL CHECK (liked IN (0, 1)),
  voter TEXT NOT NULL,
  created_at TEXT NOT NULL DEFAULT (datetime('now'))
);

-- One vote per person per set; voting again on the same set replaces it.
CREATE UNIQUE INDEX votes_once ON votes (voter, ground, text, accent);
CREATE INDEX votes_set ON votes (ground, text, accent);
