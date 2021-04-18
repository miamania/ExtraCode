import java.util.*;
import java.io.File;
import java.io.FileNotFoundException;

public class US_elections {

	public static int solution(int num_states, int[] delegates, int[] votes_Biden, int[] votes_Trump, int[] votes_Undecided) {
		//return and int representing the minimum number of people that Biden needs to convince in order to secure
		// the presidency of the United States of America, or -1 if it is impossible (Trump has already secured it)

		int total_delegates = 0;
		int Biden_delegates = 0;
		int Trump_delegates = 0;

		int[] total_state_votes = new int[num_states];
		int[] states_won = new int[num_states];
		int[] needed_to_win = new int[num_states];
		int num_undeclared = 0;

		//For each state -> Check the number of people Biden needs to win (if neither has won yet)
		for (int i=0; i < num_states; i++){
			total_delegates += delegates[i];
			total_state_votes[i] = votes_Biden[i] + votes_Trump[i] + votes_Undecided[i];

			//Check if every state has delegates and votes
			if (delegates[i] == 0 || total_state_votes[i] == 0){
				return -1;
			}

			int half_votes = (int) Math.ceil(0.5*total_state_votes[i]);

			//If Biden has more than half the total votes, he has won this state
			if (votes_Biden[i] > half_votes){
				states_won[i] = 1;
				Biden_delegates += delegates[i];

				//If Trump has at least half the votes, he wins the state
			} else if (votes_Trump[i] >= half_votes){
				states_won[i] = 0;
				Trump_delegates += delegates[i];

				//Otherwise, the state is undeclared
			} else {
				states_won[i] = -1;
				num_undeclared += 1;

				//Calculate the number of voters needed to convince to win
				if (half_votes == 0.5*total_state_votes[i]) {
					needed_to_win[i] = half_votes - votes_Biden[i] + 1;
				} else {
					needed_to_win[i] = half_votes - votes_Biden[i];
				}
			}
		}

		//Check that we have at most 2016 Delegates
		if (total_delegates > 2016){
			return -1;
		}

		int half_delegates = (int) Math.ceil(0.5*total_delegates);

		//Check if someone has already won
		if (Biden_delegates > half_delegates){
			return 0;
		} else if (Trump_delegates >= half_delegates){
			return -1;
		}

		//Check how many delegates (TOTAL) are needed to win
		int delegates_needed;
		if (half_delegates == 0.5*total_delegates) {
			delegates_needed = half_delegates - Biden_delegates + 1;
		} else {
			delegates_needed = half_delegates - Biden_delegates;
		}

		//Find arrays of the states which are still able to be won over
		//UNDECLARED STATES, UNDECLARED DELEGATES AND UNDECLARED VOTES
		int[] undeclared_states = new int[num_undeclared];
		int[] undeclared_delegates = new int[num_undeclared];
		int[] undeclared_voters = new int[num_undeclared];

		//Find total number of delegates and total number of voters which you need to win over
		int total_undeclared_delegates = 0;
		int total_undeclared_voters = 0;

		int counter = 0;
		for (int i=0; i < num_states; i++){
			if (states_won[i] == -1){
				undeclared_states[counter] = i;
				undeclared_delegates[counter] = delegates[i];
				undeclared_voters[counter] = needed_to_win[i];

				total_undeclared_delegates += delegates[i];
				total_undeclared_voters += needed_to_win[i];
				counter += 1;
			}
		}

		//If less delegates available than needed than Trump has won
		if (total_undeclared_delegates < delegates_needed){
			return -1;
		}

		//Find maximum number of delegates we can remove to still have enough delegates to win (using Knapsack)
		int max_to_remove = total_undeclared_delegates - delegates_needed;

		int i, w;
		int temp[][] = new int[num_undeclared + 1][max_to_remove + 1];

		// Build array temp[][] from bottom to the top
		//DP[i][j] is max value of ‘j-weight’ considering all values from ‘1 to ith’
		for (i = 0; i < num_undeclared + 1; i++) {
			for (w = 0; w < max_to_remove + 1; w++) {
				//Base Case
				if (i == 0 || w == 0) {
					temp[i][w] = 0;

				} else {

					//If in the state there are less/equal delegates to the current weight
					if (delegates[undeclared_states[i-1]] <= w) {

						//Take max of:
						// - number of votes needed to win in current state + total in previous square
						// - previous square
						temp[i][w] = Math.max(needed_to_win[undeclared_states[i-1]] +
								temp[i - 1][w - delegates[undeclared_states[i-1]]], temp[i - 1][w]);
					} else {
						temp[i][w] = temp[i - 1][w];
					}
				}
			}
		}

		//Return number of undeclared voters minus the maximum voters which we can eliminate -> min nb of voter needed
		return total_undeclared_voters - temp[num_undeclared][max_to_remove];

	}

	public static void main(String[] args) {
	 try {
			String path = args[0];
      File myFile = new File(path);
      Scanner sc = new Scanner(myFile);
      int num_states = sc.nextInt();
      int[] delegates = new int[num_states];
      int[] votes_Biden = new int[num_states];
      int[] votes_Trump = new int[num_states];
 			int[] votes_Undecided = new int[num_states];	
      for (int state = 0; state<num_states; state++){
			  delegates[state] =sc.nextInt();
				votes_Biden[state] = sc.nextInt();
				votes_Trump[state] = sc.nextInt();
				votes_Undecided[state] = sc.nextInt();
      }
      sc.close();
      int answer = solution(num_states, delegates, votes_Biden, votes_Trump, votes_Undecided);
      	System.out.println(answer);
    	} catch (FileNotFoundException e) {
      	System.out.println("An error occurred.");
      	e.printStackTrace();
    	}
  	}

}