import { Redis } from '@upstash/redis';

// Upstash auto-reads UPSTASH_REDIS_REST_URL + UPSTASH_REDIS_REST_TOKEN
// Vercel injects these automatically after you connect the Upstash store
const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL,
  token: process.env.UPSTASH_REDIS_REST_TOKEN,
});

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();

  /* ── POST → save tester results ─────────────────────────────── */
  if (req.method === 'POST') {
    try {
      const body = typeof req.body === 'string' ? JSON.parse(req.body) : req.body;
      const { tester, results, rows, meta } = body;

      if (!tester?.trim()) {
        return res.status(400).json({ error: 'tester name is required' });
      }

      const key = `tester:${tester.trim().toLowerCase().replace(/\s+/g, '_')}`;
      const payload = {
        tester: tester.trim(),
        saved_at: new Date().toISOString(),
        meta: meta || {},
        results: results || {},
        rows: rows || [],
      };

      await redis.set(key, JSON.stringify(payload));

      // maintain index of tester names
      const raw = await redis.get('index:testers');
      const testers = raw ? JSON.parse(raw) : [];
      if (!testers.includes(tester.trim())) {
        testers.push(tester.trim());
        await redis.set('index:testers', JSON.stringify(testers));
      }

      return res.status(200).json({ ok: true, saved_at: payload.saved_at });
    } catch (err) {
      console.error('POST error:', err);
      return res.status(500).json({ error: err.message });
    }
  }

  /* ── GET ?tester=name → load one tester ─────────────────────── */
  /* ── GET              → list all testers ────────────────────── */
  if (req.method === 'GET') {
    try {
      const { tester } = req.query;

      if (tester) {
        const key = `tester:${tester.trim().toLowerCase().replace(/\s+/g, '_')}`;
        const raw = await redis.get(key);
        if (!raw) return res.status(404).json({ error: 'not found' });
        return res.status(200).json(JSON.parse(raw));
      }

      // list all
      const indexRaw = await redis.get('index:testers');
      const names = indexRaw ? JSON.parse(indexRaw) : [];
      const summaries = await Promise.all(
        names.map(async (name) => {
          const key = `tester:${name.trim().toLowerCase().replace(/\s+/g, '_')}`;
          const raw = await redis.get(key);
          if (!raw) return null;
          const data = JSON.parse(raw);
          return { tester: data.tester, saved_at: data.saved_at, summary: data.meta?.summary || {} };
        })
      );

      return res.status(200).json({
        testers: summaries.filter(Boolean).sort((a, b) => new Date(b.saved_at) - new Date(a.saved_at)),
      });
    } catch (err) {
      console.error('GET error:', err);
      return res.status(500).json({ error: err.message });
    }
  }

  return res.status(405).json({ error: 'method not allowed' });
}
