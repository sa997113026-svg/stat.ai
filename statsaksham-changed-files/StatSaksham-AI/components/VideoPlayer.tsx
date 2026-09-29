'use client';

export type EmbedInfo = { kind: 'youtube' | 'file' | 'link' | 'none'; src: string };

// Turns whatever link was pasted into something that can actually play.
export function toEmbed(url: string): EmbedInfo {
  const u = (url || '').trim();
  if (!u) return { kind: 'none', src: '' };
  const yt = u.match(/(?:youtu\.be\/|youtube\.com\/(?:watch\?(?:.*&)?v=|embed\/|shorts\/|live\/))([A-Za-z0-9_-]{11})/);
  if (yt) return { kind: 'youtube', src: `https://www.youtube.com/embed/${yt[1]}?rel=0` };
  if (/\.(mp4|webm|ogg)(\?.*)?$/i.test(u)) return { kind: 'file', src: u };
  return { kind: 'link', src: u };
}

const box: React.CSSProperties = {
  width: '100%',
  aspectRatio: '16 / 9',
  borderRadius: 12,
  overflow: 'hidden',
  background: '#0b2b3f',
};

export default function VideoPlayer({ url, title }: { url: string; title: string }) {
  const e = toEmbed(url);

  if (e.kind === 'youtube') {
    return (
      <div style={box}>
        <iframe
          src={e.src}
          title={title}
          style={{ width: '100%', height: '100%', border: 0 }}
          allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; fullscreen"
          allowFullScreen
          referrerPolicy="strict-origin-when-cross-origin"
        />
      </div>
    );
  }

  if (e.kind === 'file') {
    return (
      <div style={box}>
        <video src={e.src} controls preload="metadata" playsInline style={{ width: '100%', height: '100%' }}>
          Your browser does not support video playback.
        </video>
      </div>
    );
  }

  return (
    <div style={{ ...box, display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#d8e7ee', textAlign: 'center', padding: 20 }}>
      {e.kind === 'link' ? (
        <span>
          This link can&apos;t be embedded.{' '}
          <a href={e.src} target="_blank" rel="noreferrer" style={{ color: '#ffb84d', textDecoration: 'underline' }}>Open it in a new tab</a>
        </span>
      ) : (
        <span>Video link not added yet — paste it into data/videos.ts</span>
      )}
    </div>
  );
}
