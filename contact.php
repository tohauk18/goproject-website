<?php
/**
 * GOPROJECT — Contact Form Handler (cPanel / ehost.pl)
 * Handles AJAX form submissions and delivers formatted emails to biuro@goproject.com.pl
 */

// Only accept POST requests
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    header('Content-Type: application/json; charset=utf-8');
    echo json_encode(['success' => false, 'error' => 'Metoda niedozwolona (Method Not Allowed).']);
    exit;
}

header('Content-Type: application/json; charset=utf-8');

// Parse request body (JSON or URL-encoded form data)
$rawInput = file_get_contents('php://input');
$data = json_decode($rawInput, true);

if (!is_array($data)) {
    $data = $_POST;
}

// 1. Honeypot Anti-Spam Check (hidden fields that humans don't fill)
if (!empty($data['_hp']) || !empty($data['website']) || !empty($data['url'])) {
    // Return fake success to stop bots from retrying
    echo json_encode(['success' => true]);
    exit;
}

// 2. Sanitize and extract input fields
function sanitize($str) {
    if (!isset($str)) return '';
    return trim(htmlspecialchars(strip_tags((string)$str), ENT_QUOTES, 'UTF-8'));
}

$name     = sanitize($data['name'] ?? $data['imie_nazwisko'] ?? '');
$phone    = sanitize($data['phone'] ?? $data['telefon'] ?? '');
$email    = filter_var(trim($data['email'] ?? ''), FILTER_SANITIZE_EMAIL);
$location = sanitize($data['location'] ?? $data['lokalizacja'] ?? '');
$service  = sanitize($data['service'] ?? 'Zapytanie ogólne');
$message  = sanitize($data['message'] ?? $data['wiadomosc'] ?? '');

// 3. Validation
if (empty($name) || empty($phone) || empty($message)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Proszę wypełnić wszystkie wymagane pola (Imię i nazwisko, Telefon, Wiadomość).']);
    exit;
}

if (!empty($email) && !filter_var($email, FILTER_VALIDATE_EMAIL)) {
    http_response_code(400);
    echo json_encode(['success' => false, 'error' => 'Podany adres e-mail ma nieprawidłowy format.']);
    exit;
}

// Prevent header injection in name or email
$name = str_replace(["\r", "\n"], '', $name);
$email = str_replace(["\r", "\n"], '', $email);

// 4. Email setup
$to = 'biuro@goproject.com.pl';
$cleanPhoneLink = preg_replace('/[^\+0-9]/', '', $phone);
$dateStr = date('Y-m-d H:i:s');

$subjectText = "Nowe zapytanie o wycenę: {$name}";
if ($service !== 'Zapytanie ogólne') {
    $subjectText .= " [{$service}]";
}
$subject = '=?UTF-8?B?' . base64_encode($subjectText) . '?=';

// HTML Email Template
$htmlBody = "
<!DOCTYPE html>
<html lang='pl'>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width, initial-scale=1.0'>
<title>Nowe zapytanie</title>
<style>
  body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background-color: #f4f4f5; margin: 0; padding: 24px; color: #18181b; }
  .wrapper { max-width: 600px; margin: 0 auto; background: #ffffff; border: 1px solid #e4e4e7; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.05); }
  .header { background: #09090b; color: #ffffff; padding: 28px 32px; border-bottom: 2px solid #e11d48; }
  .header h1 { margin: 0; font-size: 20px; font-weight: 700; letter-spacing: -0.01em; color: #ffffff; }
  .header p { margin: 6px 0 0 0; color: #a1a1aa; font-size: 13px; font-family: monospace; }
  .content { padding: 32px; }
  .field { margin-bottom: 22px; }
  .label { font-size: 11px; text-transform: uppercase; color: #71717a; font-family: monospace; letter-spacing: 0.05em; margin-bottom: 6px; font-weight: 600; }
  .value { font-size: 15px; color: #09090b; font-weight: 500; }
  .phone-btn { display: inline-block; background: #09090b; color: #ffffff !important; padding: 8px 16px; border-radius: 4px; text-decoration: none; font-weight: 600; font-size: 14px; margin-top: 4px; }
  .message-box { background: #fafafa; border: 1px solid #e4e4e7; border-left: 3px solid #e11d48; border-radius: 4px; padding: 18px; margin-top: 8px; font-size: 14px; line-height: 1.6; color: #27272a; white-space: pre-wrap; }
  .footer { border-top: 1px solid #e4e4e7; padding: 18px 32px; background: #fafafa; font-size: 12px; color: #a1a1aa; font-family: monospace; text-align: center; }
</style>
</head>
<body>
<div class='wrapper'>
  <div class='header'>
    <h1>GOPROJECT — Nowe Zapytanie z Formularza</h1>
    <p>Otrzymano: {$dateStr}</p>
  </div>
  <div class='content'>
    <div class='field'>
      <div class='label'>Klient / Inwestor</div>
      <div class='value'><strong>{$name}</strong></div>
    </div>

    <div class='field'>
      <div class='label'>Telefon</div>
      <div class='value'>
        <a href='tel:{$cleanPhoneLink}' class='phone-btn'>📞 {$phone}</a>
      </div>
    </div>";

if (!empty($email)) {
    $htmlBody .= "
    <div class='field'>
      <div class='label'>Adres E-mail</div>
      <div class='value'><a href='mailto:{$email}' style='color: #2563eb; text-decoration: underline;'>{$email}</a></div>
    </div>";
}

if (!empty($location)) {
    $htmlBody .= "
    <div class='field'>
      <div class='label'>Lokalizacja inwestycji</div>
      <div class='value'>📍 {$location}</div>
    </div>";
}

if (!empty($service)) {
    $htmlBody .= "
    <div class='field'>
      <div class='label'>Wybrana Usługa / Temat</div>
      <div class='value'>📁 <strong>{$service}</strong></div>
    </div>";
}

$htmlBody .= "
    <div class='field' style='margin-bottom: 0;'>
      <div class='label'>Wiadomość / Opis Inwestycji</div>
      <div class='message-box'>" . nl2br($message) . "</div>
    </div>
  </div>
  <div class='footer'>
    Wiadomość wysłana z formularza kontaktowego na stronie goproject.com.pl
  </div>
</div>
</body>
</html>";

// Headers
$headers = [
    'MIME-Version: 1.0',
    'Content-Type: text/html; charset=UTF-8',
    'From: GOPROJECT Formularz <biuro@goproject.com.pl>',
    'X-Mailer: PHP/' . phpversion()
];

if (!empty($email)) {
    $headers[] = "Reply-To: {$name} <{$email}>";
}

// Send mail using native server transport
$sent = @mail($to, $subject, $htmlBody, implode("\r\n", $headers));

if ($sent) {
    echo json_encode([
        'success' => true,
        'message' => 'Wiadomość została wysłana. Skontaktujemy się w ciągu 24h.'
    ]);
} else {
    // If native mail fails, return helpful error code
    http_response_code(500);
    echo json_encode([
        'success' => false,
        'error' => 'Serwer pocztowy nie mógł wysłać wiadomości. Prosimy o bezpośredni kontakt telefoniczny pod +48 884 757 815.'
    ]);
}
