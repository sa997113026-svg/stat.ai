import React, { useState } from 'react';
import { QRCodeCanvas } from 'qrcode.react';

export default function QRCodeGenerator() {
  const [text, setText] = useState('');

  return (
    <div style={{ textAlign: 'center', padding: '20px' }}>
      <h2>QR Code Generator</h2>
      <input
        type="text"
        placeholder="Enter URL or text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        style={{ padding: '8px', width: '250px', marginRight: '10px' }}
      />

      <div style={{ marginTop: '20px' }}>
        {text ? (
          <QRCodeCanvas value={text} size={200} />
        ) : (
          <p>Enter text above to preview QR code</p>
        )}
      </div>
    </div>
  );
}
