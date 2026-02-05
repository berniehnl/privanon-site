<?php
header('Content-Type: application/json');

// prevent direct access
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['status' => 'error', 'message' => 'Method not allowed']);
    exit;
}

// Configuration
$to_email = 'contact@privanon.com'; // Update this with your actual receiving email if different
$subject_prefix = '[Privanon Website Inquiry]';

// Sanitize and Validate Input
$name = filter_input(INPUT_POST, 'name', FILTER_SANITIZE_STRING);
$email = filter_input(INPUT_POST, 'email', FILTER_VALIDATE_EMAIL);
$organization = filter_input(INPUT_POST, 'organization', FILTER_SANITIZE_STRING);
$interest = filter_input(INPUT_POST, 'interest', FILTER_SANITIZE_STRING);
$message = filter_input(INPUT_POST, 'message', FILTER_SANITIZE_STRING);

// Basic Validation
if (!$name || !$email || !$message) {
    http_response_code(400);
    echo json_encode(['status' => 'error', 'message' => 'Please fill in all required fields.']);
    exit;
}

// Construct Email Body
$email_subject = "$subject_prefix $interest - from $name";
$email_body = "New inquiry received from Privanon.com:\n\n";
$email_body .= "Name: $name\n";
$email_body .= "Email: $email\n";
$email_body .= "Organization: " . ($organization ? $organization : 'N/A') . "\n";
$email_body .= "Area of Interest: $interest\n\n";
$email_body .= "Message:\n$message\n";

// Headers
$headers = "From: no-reply@privanon.com\r\n";
$headers .= "Reply-To: $email\r\n";
$headers .= "X-Mailer: PHP/" . phpversion();

// Send Email
try {
    if (mail($to_email, $email_subject, $email_body, $headers)) {
        echo json_encode(['status' => 'success', 'message' => 'Message sent successfully.']);
    } else {
        throw new Exception('Mail transmission failed.');
    }
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['status' => 'error', 'message' => 'Server error: Unable to send message.']);
}
?>
