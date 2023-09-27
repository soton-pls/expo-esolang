`default_nettype none

module hanoi #(
	parameter int N = 3,
	parameter int PROG_SIZE = 8
) (
	input logic clk
);

// A space of 1 to store the trap condition at the end that causes execution
// to halt
localparam int MEM_SIZE = PROG_SIZE + 1;
localparam int PC_BITS = $clog2(MEM_SIZE);

typedef logic [PC_BITS-1:0] pc_t;
typedef logic [N-1:0] set_t;

typedef enum logic [2:0] {
	TOK_LEFT = 0,
	TOK_RIGHT,
	TOK_INTERACT,
	TOK_LOOP_BEGIN,
	TOK_LOOP_END,
	TOK_SWAP,
	TOK_NOP
} token_t;

token_t mem [0:MEM_SIZE-1];

pc_t pc_r, pc_nxt;
logic [1:0] pointer_r, pointer_nxt;

set_t state_r [0:2], state_nxt [0:2];
set_t held_r, held_nxt;
set_t bag_r, bag_nxt;

initial begin
	pc_r             = '0;
	pointer_r        = '0;
	state_r[0]       = '1;
	state_r[1]       = '0;
	state_r[2]       = '0;
	held_r           = '0;
	bag_r            = '0;
end

// All symbols but the last one are not NOPs (so the program is exactly the
// specified length)
always_comb
	foreach(mem[i])
		assume(i == MEM_SIZE - 1 ? mem[i] == TOK_NOP : mem[i] < TOK_NOP);

// Assume there are as many loop starts as ends (as needed for well-formed
// programs)
always_comb begin
	pc_t begin_count = '0, end_count = '0;
	foreach (mem[i]) begin
		begin_count += PC_BITS'(mem[i] == TOK_LOOP_BEGIN);
		end_count += PC_BITS'(mem[i] == TOK_LOOP_END);
	end
	assume(begin_count == end_count);
end

// Get a set vector which just has the bit set corresponding to the top bit
// of set
function set_t top_set(input set_t set);
	begin
		top_set = '0;
		for (int i = 0; i < N; i++) begin
			if (set[N-i-1] && top_set == '0)
				top_set[N-i-1] = 1'b1;
		end
	end
endfunction

token_t token;
assign token = mem[pc_r];

always_comb begin
	pc_nxt             = pc_r + PC_BITS'(1'b1);
	pointer_nxt        = pointer_r;
	state_nxt          = state_r;
	held_nxt           = held_r;
	bag_nxt            = bag_r;

	case (token)
		TOK_LEFT:  pointer_nxt = (pointer_r == '0) ? 2'd2 : pointer_r - 2'd1;
		TOK_RIGHT: pointer_nxt = (pointer_r + 2'd1) % 2'd3;
		TOK_INTERACT: begin
			if (held_r == '0) begin
				held_nxt              = top_set(state_r[pointer_r]);
				state_nxt[pointer_r] &= ~top_set(state_r[pointer_r]);
			end
			// high bits of held_r represent smaller items
			else if (held_r > state_r[pointer_r]) begin
				held_nxt              = '0;
				state_nxt[pointer_r] |= held_r;
			end
		end
		TOK_LOOP_BEGIN: begin
			// Find jump target
			pc_t count = '0;
			logic found = '0;
			foreach (mem[i]) begin
				if (i >= pc_r) begin
					count += PC_BITS'(mem[i] == TOK_LOOP_BEGIN);
					count -= PC_BITS'(mem[i] == TOK_LOOP_END);
					if (count == '0) begin
						if (held_r == '0)
							pc_nxt = PC_BITS'(i) + 1'b1;
						found = '1;
						break;
					end
				end
			end
			assume(found);
		end
		TOK_LOOP_END: begin
			// Find backjump target
			pc_t count = '0;
			logic found = '0;
			foreach (mem[i]) begin
				int j = MEM_SIZE-i-1;
				if (j <= pc_r) begin
					count += PC_BITS'(mem[j] == TOK_LOOP_BEGIN);
					count -= PC_BITS'(mem[j] == TOK_LOOP_END);
					if (count == '0) begin
						if (held_r != '0)
							pc_nxt = PC_BITS'(j) + 1'b1;
						found = '1;
						break;
					end
				end
			end
			assume(found);
		end
		TOK_SWAP: begin
			held_nxt = bag_r;
			bag_nxt  = held_r;
		end
		default: pc_nxt = pc_r;
	endcase
end

always_ff @(posedge clk) begin
	pc_r           <= pc_nxt;
	pointer_r      <= pointer_nxt;
	state_r        <= state_nxt;
	held_r         <= held_nxt;
	bag_r          <= bag_nxt;
	mem            <= mem;
end

always_comb begin
	// Check we never reach a state where either of the non-original stacks
	// is full
	assert(!(state_r[2] == '1 || state_r[1] == '1));

	// Used for case split
`ifdef FIRST_TOK
	assume(mem[0] == `FIRST_TOK);
`endif
end

logic [1:0] past_valid;
initial past_valid = '0;
always_ff @(posedge clk) past_valid <= {past_valid[0:0], '1};

// Helper invariants - These are true facts that define more of the statespace
// as bad. This makes it easier for the model checker to prove the target
// assertion true
always_comb begin
	assert((state_r[0] & state_r[1]) == '0);
	assert((state_r[1] & state_r[2]) == '0);
	assert((state_r[0] & state_r[2]) == '0);
	assert((state_r[0] & held_r) == '0);
	assert((state_r[1] & held_r) == '0);
	assert((state_r[2] & held_r) == '0);
	assert((state_r[0] & bag_r) == '0);
	assert((state_r[1] & bag_r) == '0);
	assert((state_r[2] & bag_r) == '0);
	assert((held_r & bag_r) == '0);
	assert($onehot0(held_r));
	assert($onehot0(bag_r));
	assert((state_r[0] | state_r[1] | state_r[2] | held_r | bag_r) == '1);

	assert(mem[0] != TOK_LOOP_END);
	if (past_valid[0])
		assert(pc_r >= 'd1);
	if (past_valid[1])
		assert(pc_r >= 'd2);
end

endmodule
