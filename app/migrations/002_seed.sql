-- 002: Demodaten. INSERT OR IGNORE, damit die Migration idempotent ist.
INSERT OR IGNORE INTO members (id, name, email, team, is_admin) VALUES
    (1, 'Dana Berger',    'dana.berger@example.com',    'Platform',  1),
    (2, 'Tom Vogel',      'tom.vogel@example.com',      'Frontend',  0),
    (3, 'Aylin Kaya',     'aylin.kaya@example.com',     'Data',      0),
    (4, 'Jonas Richter',  'jonas.richter@example.com',  'QA',        0),
    (5, 'Mira Schulz',    'mira.schulz@example.com',    'Frontend',  0);

INSERT OR IGNORE INTO items (id, name, category, inventory_no, status, notes) VALUES
    (1,  'ThinkPad X1 Carbon',     'Laptop',    'INV-0001', 'on_loan',     '16 GB RAM, Docking-Station im Schrank'),
    (2,  'MacBook Pro 14"',        'Laptop',    'INV-0002', 'available',   NULL),
    (3,  'Epson EB-L200 Beamer',   'Beamer',    'INV-0003', 'on_loan',     'HDMI-Kabel liegt bei'),
    (4,  'Sony A7 IV',             'Kamera',    'INV-0004', 'available',   'Nur mit Tasche ausleihen'),
    (5,  'Rode Wireless GO II',    'Audio',     'INV-0005', 'on_loan',     NULL),
    (6,  'iPad Pro 12.9"',         'Tablet',    'INV-0006', 'maintenance', 'Display-Riss, beim Service'),
    (7,  'Logitech Brio Webcam',   'Zubehör',   'INV-0007', 'available',   NULL),
    (8,  'Jabra Speak 750',        'Audio',     'INV-0008', 'on_loan',     NULL),
    (9,  'USB-C Dock (Dell WD19)', 'Zubehör',   'INV-0009', 'available',   NULL),
    (10, 'Pixel 8 Testgerät',      'Smartphone','INV-0010', 'available',   'Android 15, Testaccount siehe Wiki');

INSERT OR IGNORE INTO loans (id, item_id, member_id, loaned_at, due_date, returned_at) VALUES
    (1, 1, 2, '2026-09-01', '2026-09-15', NULL),         -- überfällig
    (2, 3, 3, '2026-09-10', '2026-09-24', NULL),
    (3, 5, 2, '2026-08-20', '2026-09-03', NULL),         -- überfällig
    (4, 8, 4, '2026-09-18', '2026-10-02', NULL),
    (5, 2, 1, '2026-08-01', '2026-08-15', '2026-08-14'), -- zurückgegeben
    (6, 4, 5, '2026-07-05', '2026-07-19', '2026-07-22'); -- verspätet zurückgegeben
