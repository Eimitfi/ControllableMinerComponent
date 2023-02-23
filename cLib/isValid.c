#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include "sha3/sph_blake.h"
#include "sha3/sph_keccak.h"
#include "sha3/sph_cubehash.h"
#include "sha3/sph_skein.h"
#include "sha3/sph_groestl.h"
#include "lyra2/Lyra2.h"

#include <stdio.h>

void allium_hash(void *state, const void *input)
{
	uint32_t hashA[8], hashB[8];

	sph_blake256_context     ctx_blake;
	sph_keccak256_context    ctx_keccak;
	sph_skein256_context     ctx_skein;
	sph_groestl256_context   ctx_groestl;
	sph_cubehash256_context  ctx_cube;

	// sph_blake256_set_rounds(14);

	sph_blake256_init(&ctx_blake);
	sph_blake256(&ctx_blake, input, 80);
	sph_blake256_close(&ctx_blake, hashA);

	sph_keccak256_init(&ctx_keccak);
	sph_keccak256(&ctx_keccak, hashA, 32);
	sph_keccak256_close(&ctx_keccak, hashB);

	LYRA2(hashA, 32, hashB, 32, hashB, 32, 1, 8, 8);

	sph_cubehash256_init(&ctx_cube);
	sph_cubehash256(&ctx_cube, hashA, 32);
	sph_cubehash256_close(&ctx_cube, hashB);

	LYRA2(hashA, 32, hashB, 32, hashB, 32, 1, 8, 8);

	sph_skein256_init(&ctx_skein);
	sph_skein256(&ctx_skein, hashA, 32);
	sph_skein256_close(&ctx_skein, hashB);

	sph_groestl256_init(&ctx_groestl);
	sph_groestl256(&ctx_groestl, hashB, 32);
	sph_groestl256_close(&ctx_groestl, hashA);

	memcpy(state, hashA, 32);
}

static inline void le32enc(void *pp, uint32_t x)
{
	uint8_t *p = (uint8_t *)pp;
	p[0] = x & 0xff;
	p[1] = (x >> 8) & 0xff;
	p[2] = (x >> 16) & 0xff;
	p[3] = (x >> 24) & 0xff;
}

bool fulltest(const uint32_t *hash, const uint32_t *target)
{
	int i;
	unsigned int rc = true;
	
	for (i = 7; i >= 0; i--) {
		if (hash[i] > target[i]) {
			rc = false;
			break;
		}
		if (hash[i] < target[i]) {
			rc = true;
			break;
		}
	}
	return rc;
}


/*this is mine*/
bool isValid(uint64_t nonce[1], const uint32_t target[8], uint32_t netheader[19]){
	uint32_t hashed[8],header[20];
	for(int i = 0;i < 19;i++){
		header[i] = netheader[i];
	}
	(*nonce)++;
	le32enc(&header[19],(uint32_t)nonce[0]);
	allium_hash(hashed,header);
	return fulltest(hashed,target);
}
