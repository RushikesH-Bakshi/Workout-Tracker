import Link from 'next/link';

export default function Home() {
  return (
    <section>
      <div className="hero">
        <div>
          <h1 className="page-title">Welcome to Workout Logger</h1>
          <p>
            Track your push-ups, manage workouts, and review progress with a clean React-based frontend.
          </p>
          <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap', marginTop: '24px' }}>
            <Link href="/signup">
              <a className="button">Get Started</a>
            </Link>
            <Link href="/login">
              <a className="button secondary">Browse Workouts</a>
            </Link>
          </div>
        </div>

        <img src="/images/pushup.png" alt="Workout" />
      </div>
    </section>
  );
}
