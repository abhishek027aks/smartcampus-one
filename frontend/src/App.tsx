import { FormEvent, useEffect, useRef, useState } from "react";

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";

type User = {
  id: number;
  full_name: string;
  email: string;
  role: string;
  college_id: number | null;
};

type AttendanceSession = {
  session_id: number;
  session_code: string;
  started_at: string;
  expires_at: string;
  is_active: boolean;
};

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const token = localStorage.getItem("smartcampus_token");

    if (!token) {
      return;
    }

    fetch(`${API_BASE_URL}/auth/me`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then(async (response) => {
        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || "Session expired.");
        }

        setUser(data);
      })
      .catch(() => {
        localStorage.removeItem("smartcampus_token");
      });
  }, []);

  async function handleLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();

    setError("");
    setLoading(true);

    try {
      const body = new URLSearchParams();

      body.set("username", email);
      body.set("password", password);
      body.set("grant_type", "password");

      const loginResponse = await fetch(`${API_BASE_URL}/auth/login`, {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
        },
        body,
      });

      const loginData = await loginResponse.json();

      if (!loginResponse.ok) {
        throw new Error(loginData.detail || "Invalid email or password.");
      }

      localStorage.setItem("smartcampus_token", loginData.access_token);

      const meResponse = await fetch(`${API_BASE_URL}/auth/me`, {
        headers: {
          Authorization: `Bearer ${loginData.access_token}`,
        },
      });

      const meData = await meResponse.json();

      if (!meResponse.ok) {
        throw new Error(meData.detail || "Unable to load user profile.");
      }

      setUser(meData);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed.");
    } finally {
      setLoading(false);
    }
  }

  function logout() {
    localStorage.removeItem("smartcampus_token");
    setUser(null);
    setError("");
    setEmail("");
    setPassword("");
  }

  if (user?.role === "student") {
    return <StudentDashboard user={user} logout={logout} />;
  }

  if (user) {
    return <TeacherDashboard user={user} logout={logout} />;
  }

  return (
    <main className="app-shell">
      <section className="login-layout">
        <div className="hero-panel">
          <div className="brand-mark large">SC</div>

          <p className="eyebrow">SMARTCAMPUS ONE</p>

          <h1>One Smart Platform for Every Campus.</h1>

          <p className="hero-text">
            Smart timetable, attendance and campus management in one
            secure platform.
          </p>

          <div className="hero-points">
            <span>✓ Multi-college platform</span>
            <span>✓ Smart timetable management</span>
            <span>✓ Secure attendance</span>
          </div>
        </div>

        <div className="login-card">
          <div className="login-heading">
            <p className="eyebrow">SECURE ACCESS</p>

            <h2>Sign in</h2>

            <p>
              Use your SmartCampus One account to continue.
            </p>
          </div>

          <form onSubmit={handleLogin}>
            <label htmlFor="email">Email address</label>

            <input
              id="email"
              type="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="you@college.edu"
              autoComplete="email"
              required
            />

            <label htmlFor="password">Password</label>

            <input
              id="password"
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              placeholder="Enter your password"
              autoComplete="current-password"
              required
            />

            {error && <div className="error-box">{error}</div>}

            <button
              className="login-button"
              type="submit"
              disabled={loading}
            >
              {loading ? "Signing in..." : "Sign in"}
            </button>
          </form>

          <p className="login-footer">
            SmartCampus One · Secure Campus Management
          </p>
        </div>
      </section>
    </main>
  );
}

function TeacherDashboard({
  user,
  logout,
}: {
  user: User;
  logout: () => void;
}) {
  const [error, setError] = useState("");
  const [session, setSession] = useState<AttendanceSession | null>(null);
  const [sessionLoading, setSessionLoading] = useState(false);
  const [remainingSeconds, setRemainingSeconds] = useState(0);

  useEffect(() => {
    const currentSession = session;

    if (!currentSession) {
      setRemainingSeconds(0);
      return;
    }

    function updateTimer() {
      const expiry = new Date(currentSession!.expires_at).getTime();
      const remaining = Math.max(
        0,
        Math.floor((expiry - Date.now()) / 1000),
      );

      setRemainingSeconds(remaining);

      if (remaining === 0) {
        setSession((current) =>
          current ? { ...current, is_active: false } : current,
        );
      }
    }

    updateTimer();

    const timer = window.setInterval(updateTimer, 1000);

    return () => window.clearInterval(timer);
  }, [session]);

  async function startAttendance() {
    const token = localStorage.getItem("smartcampus_token");

    if (!token) {
      setError("Please sign in again.");
      return;
    }

    setSessionLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_BASE_URL}/attendance/sessions/start?section_id=1&subject_id=1&teacher_id=1&duration_minutes=5`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to start attendance.");
      }

      setSession(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to start attendance.",
      );
    } finally {
      setSessionLoading(false);
    }
  }

  async function closeAttendance() {
    if (!session) {
      return;
    }

    const token = localStorage.getItem("smartcampus_token");

    if (!token) {
      setError("Please sign in again.");
      return;
    }

    setSessionLoading(true);
    setError("");

    try {
      const response = await fetch(
        `${API_BASE_URL}/attendance/sessions/${session.session_id}/close`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to close attendance.");
      }

      setSession((current) =>
        current ? { ...current, is_active: false } : current,
      );
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to close attendance.",
      );
    } finally {
      setSessionLoading(false);
    }
  }

  function formatTime(totalSeconds: number) {
    const minutes = Math.floor(totalSeconds / 60)
      .toString()
      .padStart(2, "0");

    const seconds = (totalSeconds % 60)
      .toString()
      .padStart(2, "0");

    return `${minutes}:${seconds}`;
  }

  return (
    <main className="app-shell">
      <section className="dashboard-card">
        <header className="dashboard-header">
          <div className="brand-row">
            <div className="brand-mark">SC</div>

            <div>
              <p className="eyebrow">SMARTCAMPUS ONE</p>
              <h1>
                Welcome, {user.full_name || "Teacher"}
              </h1>
            </div>
          </div>

          <button className="logout-button" onClick={logout}>
            Sign out
          </button>
        </header>

        <div className="profile-card">
          <div>
            <span className="profile-label">ROLE</span>
            <strong>
              {user.role.replace("_", " ").toUpperCase()}
            </strong>
          </div>

          <div>
            <span className="profile-label">EMAIL</span>
            <span className="profile-email">{user.email}</span>
          </div>

          <div>
            <span className="profile-label">COLLEGE</span>
            <span className="profile-email">
              College #{user.college_id ?? "Platform"}
            </span>
          </div>
        </div>

        {error && <div className="error-box">{error}</div>}

        <section className="attendance-section">
          <div className="section-heading">
            <div>
              <p className="eyebrow">SMART ATTENDANCE</p>
              <h2>Attendance Control</h2>
              <p>
                Start a temporary attendance session and display
                the code to students.
              </p>
            </div>

            {!session?.is_active && (
              <button
                className="primary-action"
                onClick={startAttendance}
                disabled={sessionLoading}
              >
                {sessionLoading
                  ? "Starting..."
                  : "Start Attendance"}
              </button>
            )}
          </div>

          {session && (
            <div
              className={
                session.is_active
                  ? "session-card active"
                  : "session-card closed"
              }
            >
              <div className="session-top">
                <div>
                  <span className="session-status">
                    {session.is_active
                      ? "● LIVE SESSION"
                      : "● CLOSED"}
                  </span>

                  <h3>
                    Attendance Session #{session.session_id}
                  </h3>
                </div>

                {session.is_active && (
                  <div className="timer">
                    {formatTime(remainingSeconds)}
                  </div>
                )}
              </div>

              {session.is_active ? (
                <>
                  <div className="code-box">
                    <span>ATTENDANCE CODE</span>
                    <strong>{session.session_code}</strong>
                    <small>
                      Students must enter this temporary code.
                    </small>
                  </div>

                  <button
                    className="close-session-button"
                    onClick={closeAttendance}
                    disabled={sessionLoading}
                  >
                    {sessionLoading
                      ? "Closing..."
                      : "Close Attendance Session"}
                  </button>
                </>
              ) : (
                <div className="closed-message">
                  This attendance session is no longer active.
                </div>
              )}
            </div>
          )}
        </section>

        <section className="dashboard-grid">
          <div className="feature-card">
            <span>📅</span>
            <h3>Timetable</h3>
            <p>
              View and manage your assigned classes and schedule.
            </p>
          </div>

          <div className="feature-card">
            <span>✓</span>
            <h3>Attendance</h3>
            <p>
              Start sessions and securely collect student attendance.
            </p>
          </div>

          <div className="feature-card">
            <span>📊</span>
            <h3>Analytics</h3>
            <p>
              Monitor attendance percentage and academic activity.
            </p>
          </div>
        </section>
      </section>
    </main>
  );
}

function StudentDashboard({
  user,
  logout,
}: {
  user: User;
  logout: () => void;
}) {
  const [sessionId, setSessionId] = useState("");
  const [sessionCode, setSessionCode] = useState("");
  const [cameraOpen, setCameraOpen] = useState(false);
  const [capturedPhoto, setCapturedPhoto] = useState<Blob | null>(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  const videoRef = useRef<HTMLVideoElement | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  async function openCamera() {
    setError("");
    setMessage("");
    setCapturedPhoto(null);
    setPreviewUrl("");

    if (!sessionId.trim()) {
      setError("Enter the attendance session ID first.");
      return;
    }

    if (!sessionCode.trim()) {
      setError("Enter the attendance code first.");
      return;
    }

    if (!navigator.mediaDevices?.getUserMedia) {
      setError(
        "Camera access is not supported by this browser.",
      );
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: "user",
          width: { ideal: 1280 },
          height: { ideal: 720 },
        },
        audio: false,
      });

      streamRef.current = stream;
      setCameraOpen(true);

      window.setTimeout(() => {
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          videoRef.current.play().catch(() => {});
        }
      }, 50);
    } catch {
      setError(
        "Camera permission was denied or the camera is unavailable.",
      );
    }
  }

  function closeCamera() {
    streamRef.current?.getTracks().forEach((track) => {
      track.stop();
    });

    streamRef.current = null;
    setCameraOpen(false);
  }

  function capturePhoto() {
    const video = videoRef.current;
    const canvas = canvasRef.current;

    if (!video || !canvas) {
      setError("Camera is not ready.");
      return;
    }

    if (!video.videoWidth || !video.videoHeight) {
      setError("Camera is still starting. Please wait a moment.");
      return;
    }

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const context = canvas.getContext("2d");

    if (!context) {
      setError("Unable to capture camera image.");
      return;
    }

    context.drawImage(
      video,
      0,
      0,
      canvas.width,
      canvas.height,
    );

    canvas.toBlob(
      (blob) => {
        if (!blob) {
          setError("Unable to create photo.");
          return;
        }

        setCapturedPhoto(blob);

        const url = URL.createObjectURL(blob);
        setPreviewUrl((oldUrl) => {
          if (oldUrl) {
            URL.revokeObjectURL(oldUrl);
          }

          return url;
        });

        closeCamera();
        setMessage(
          "Live photo captured. Review it and submit attendance.",
        );
      },
      "image/jpeg",
      0.88,
    );
  }

  async function submitAttendance() {
    if (!capturedPhoto) {
      setError("Capture a live photo before submitting.");
      return;
    }

    if (!sessionId.trim() || !sessionCode.trim()) {
      setError("Session ID and attendance code are required.");
      return;
    }

    const token = localStorage.getItem("smartcampus_token");

    if (!token) {
      setError("Please sign in again.");
      return;
    }

    setLoading(true);
    setError("");
    setMessage("");

    try {
      const body = new FormData();

      body.append("student_id", String(user.id === 2 ? 1 : user.id));
      body.append("session_code", sessionCode.trim());
      body.append(
        "photo",
        capturedPhoto,
        "live-attendance.jpg",
      );

      const response = await fetch(
        `${API_BASE_URL}/attendance/sessions/${sessionId.trim()}/mark`,
        {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
          },
          body,
        },
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail || "Unable to mark attendance.",
        );
      }

      setMessage(
        `Attendance marked successfully. Attendance ID: ${data.attendance_id}`,
      );

      setCapturedPhoto(null);

      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }

      setPreviewUrl("");
      setSessionCode("");
      setSessionId("");
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Unable to mark attendance.",
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    return () => {
      streamRef.current?.getTracks().forEach((track) => {
        track.stop();
      });

      if (previewUrl) {
        URL.revokeObjectURL(previewUrl);
      }
    };
  }, [previewUrl]);

  return (
    <main className="app-shell">
      <section className="dashboard-card student-dashboard">
        <header className="dashboard-header">
          <div className="brand-row">
            <div className="brand-mark">SC</div>

            <div>
              <p className="eyebrow">SMARTCAMPUS ONE</p>
              <h1>
                Welcome, {user.full_name || "Student"}
              </h1>
            </div>
          </div>

          <button className="logout-button" onClick={logout}>
            Sign out
          </button>
        </header>

        <div className="profile-card">
          <div>
            <span className="profile-label">ROLE</span>
            <strong>STUDENT</strong>
          </div>

          <div>
            <span className="profile-label">EMAIL</span>
            <span className="profile-email">{user.email}</span>
          </div>

          <div>
            <span className="profile-label">COLLEGE</span>
            <span className="profile-email">
              College #{user.college_id ?? "-"}
            </span>
          </div>
        </div>

        <section className="student-attendance-card">
          <div className="student-title">
            <div>
              <p className="eyebrow">STUDENT ATTENDANCE</p>
              <h2>Mark Your Attendance</h2>
              <p>
                Enter the temporary code shown by your teacher,
                then capture a live photo using your device camera.
              </p>
            </div>

            <div className="security-badge">
              🔒 Code + Live Photo
            </div>
          </div>

          <div className="student-form">
            <div>
              <label htmlFor="sessionId">
                Attendance Session ID
              </label>

              <input
                id="sessionId"
                type="number"
                min="1"
                value={sessionId}
                onChange={(event) =>
                  setSessionId(event.target.value)
                }
                placeholder="Example: 3"
              />
            </div>

            <div>
              <label htmlFor="sessionCode">
                Attendance Code
              </label>

              <input
                id="sessionCode"
                type="text"
                inputMode="numeric"
                maxLength={6}
                value={sessionCode}
                onChange={(event) =>
                  setSessionCode(
                    event.target.value.replace(/\D/g, ""),
                  )
                }
                placeholder="6-digit code"
              />
            </div>
          </div>

          {error && <div className="error-box">{error}</div>}

          {message && (
            <div className="success-box">{message}</div>
          )}

          {!cameraOpen && !capturedPhoto && (
            <button
              className="camera-button"
              onClick={openCamera}
            >
              📷 Open Camera
            </button>
          )}

          {cameraOpen && (
            <div className="camera-panel">
              <video
                ref={videoRef}
                className="camera-preview"
                autoPlay
                playsInline
                muted
              />

              <div className="camera-warning">
                Live camera capture is required. Gallery upload is
                not available.
              </div>

              <div className="camera-actions">
                <button
                  className="capture-button"
                  onClick={capturePhoto}
                >
                  Capture Live Photo
                </button>

                <button
                  className="cancel-camera-button"
                  onClick={closeCamera}
                >
                  Cancel
                </button>
              </div>
            </div>
          )}

          <canvas
            ref={canvasRef}
            className="hidden-canvas"
          />

          {capturedPhoto && previewUrl && (
            <div className="photo-review">
              <p className="review-title">
                LIVE PHOTO PREVIEW
              </p>

              <img
                src={previewUrl}
                alt="Captured attendance preview"
              />

              <div className="review-actions">
                <button
                  className="camera-button"
                  onClick={openCamera}
                >
                  Retake Photo
                </button>

                <button
                  className="submit-attendance-button"
                  onClick={submitAttendance}
                  disabled={loading}
                >
                  {loading
                    ? "Submitting..."
                    : "Submit Attendance"}
                </button>
              </div>
            </div>
          )}
        </section>

        <section className="dashboard-grid">
          <div className="feature-card">
            <span>📅</span>
            <h3>Timetable</h3>
            <p>
              View your daily and weekly class schedule.
            </p>
          </div>

          <div className="feature-card">
            <span>✓</span>
            <h3>Attendance</h3>
            <p>
              Mark attendance securely with code and live photo.
            </p>
          </div>

          <div className="feature-card">
            <span>📊</span>
            <h3>My Analytics</h3>
            <p>
              View attendance percentage and academic progress.
            </p>
          </div>
        </section>
      </section>
    </main>
  );
}

export default App;

