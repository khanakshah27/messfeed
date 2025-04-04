<?php
session_start();
require_once 'db_connect.php';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    if (!isset($_SESSION['user_id'])) {
        echo json_encode(['success' => false, 'message' => 'User not logged in']);
        exit;
    }

    $user_id = $_SESSION['user_id'];
    $feedback = trim($_POST['feedback']);

    if (empty($feedback)) {
        echo json_encode(['success' => false, 'message' => 'Feedback cannot be empty']);
        exit;
    }

    try {
        $stmt = $conn->prepare("INSERT INTO feedback (user_id, feedback) VALUES (?, ?)");
        $stmt->execute([$user_id, $feedback]);

        echo json_encode(['success' => true, 'message' => 'Feedback submitted successfully']);
    } catch (PDOException $e) {
        echo json_encode(['success' => false, 'message' => 'Error submitting feedback']);
    }
}
?>
