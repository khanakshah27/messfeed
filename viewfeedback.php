<?php
session_start();
require_once 'db_connect.php';

if (!isset($_SESSION['user_type']) || $_SESSION['user_type'] !== 'admin') {
    echo json_encode(['success' => false, 'message' => 'Access denied']);
    exit;
}

try {
    $stmt = $conn->prepare("
        SELECT f.id, u.reg_number, f.feedback, f.timestamp 
        FROM feedback f
        JOIN users u ON f.user_id = u.id
        ORDER BY f.timestamp DESC
    ");
    $stmt->execute();
    $feedbacks = $stmt->fetchAll(PDO::FETCH_ASSOC);

    echo json_encode(['success' => true, 'feedbacks' => $feedbacks]);
} catch (PDOException $e) {
    echo json_encode(['success' => false, 'message' => 'Error retrieving feedback']);
}
?>
