import "./Stats.css";
import { useSetting } from "./util";

export interface StatProps {
  gameNumberLastPlayed: number;
  gameNumberLastStarted: number;
  lostGameLastPlayed: boolean;
  nPlayed: number;
  nWon: number;
  counts: Array<number>;
  guesses: Array<string>;
}

export function defaultStats() {
  return {'nPlayed': 0, 'nWon': 0,
    'gameNumberLastPlayed': 0,
    'gameNumberLastStarted': 0,
    'lostGameLastPlayed': false,
    'counts': [0, 0, 0, 0, 0, 0, 0], 'guesses': []};
}

export function updateGuesses(stats: StatProps, guesses: string[], gameNumber: number, lastGuess: string) {
  stats.gameNumberLastStarted = gameNumber;
  stats.guesses = guesses.concat([lastGuess]);
  return stats;
}

export function updateStats(stats: StatProps, guesses: string[], lost: boolean, gameNumber: number, lastGuess: string) {
  stats.gameNumberLastPlayed = gameNumber;
  stats.gameNumberLastStarted = gameNumber;
  stats.nPlayed++;
  stats.guesses = guesses.concat([lastGuess]);
  stats.lostGameLastPlayed = lost;
  if (lost) {
    stats.counts[stats.counts.length-1]++;
  } else {
    stats.counts[guesses.length]++;
    stats.nWon++;
  }
  return stats;
}

function getHistWidth(value: number, sum: number) {
  if (sum > 0) {
    return Math.round(200 * value/sum);
  } else {
    return 0;
  }
}

function makeHistogram(index: string, value: number, max: number) {
  return (<div className="graph-container">
          <div className="guess">{ index }</div>
          <div className="graph">
            <div className="graph-bar align-right" style={{ width: getHistWidth(value, max) }}>
              <div className="num-guesses">{value}</div>
            </div>
          </div>
        </div>);
}

export function Stats() {
  const [stats, setStats] = useSetting<StatProps>("stats", defaultStats());
  const maxCount = Math.max(...stats.counts);
  return (
    <div className="App-stats">
      <h2>STATISTICS</h2>
      <p>Played { stats.nPlayed } games, Won { stats.nPlayed ? Math.round(100*(stats.nWon / stats.nPlayed)): 0 }%</p>

      <div className="histograms">
        { makeHistogram('1', stats.counts[0], maxCount) }
        { makeHistogram('2', stats.counts[1], maxCount) }
        { makeHistogram('3', stats.counts[2], maxCount) }
        { makeHistogram('4', stats.counts[3], maxCount) }
        { makeHistogram('5', stats.counts[4], maxCount) }
        { makeHistogram('6', stats.counts[5], maxCount) }
        { makeHistogram('X', stats.counts[6], maxCount) }
      </div>
    </div>
  );
}
