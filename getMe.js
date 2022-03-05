const fs = require('fs')
const SpotifyWebApi = require('spotify-web-api-node');
const token = "BQDS0mjMSNl2yJP8w0KfEmJvs2uDcBFHV0LxF0hi8ddAdo73Cb8-6kMcZeFnigl_7nm7pMBkgDfKy9DY2mBq5Rftg2B0EUh_wrrCFOJTllYP-xvmUKkAXcAZkDWrGX1he99GM6PwtmEoEh2VTYM4h40CKqU_KdiFNCtmHi_1FMqHtxJyuOWInyf6BiZHmRHS_a1AdyUI09Qy6QMPnSAyhgTFUl8nTtiYTlEzOOcVX9p00FX0HW3Z2Fdb5HAX1EWxTARe8sPoS2fNHWcyg_m1YfhvmJBuLqCTDJHCbfvm7wxnnkdnBl54";

const spotifyApi = new SpotifyWebApi();
spotifyApi.setAccessToken(token);

//GET MY PROFILE DATA
function getMyData() {
  (async () => {
    const me = await spotifyApi.getMe();
    // console.log(me.body);
    searchPlaylist('happy')
  })().catch(e => {
    console.error(e);
  });
}

//GET MY PLAYLISTS

async function searchPlaylist(keyword) {
  const data = await spotifyApi.searchPlaylists(keyword)
  let playlists = []

  console.log("searching", data.body.playlists.items[0].name)
  for (let playlist of data.body.playlists.items) {
    console.log(playlist.name)
  }

}


async function getUserPlaylists(userName) {
  const data = await spotifyApi.getUserPlaylists(userName)

  console.log("---------------+++++++++++++++++++++++++")
  let playlists = []

  for (let playlist of data.body.items) {
    console.log(playlist.name + " " + playlist.id)
    
    let tracks = await getPlaylistTracks(playlist.id, playlist.name);
    // console.log(tracks);

    const tracksJSON = { tracks }
    let data = JSON.stringify(tracksJSON);
    fs.writeFileSync(playlist.name+'.json', data);
  }
}

//GET SONGS FROM PLAYLIST
async function getPlaylistTracks(playlistId, playlistName) {

  const data = await spotifyApi.getPlaylistTracks(playlistId, {
    offset: 1,
    limit: 100,
    fields: 'items'
  })

  // console.log('The playlist contains these tracks', data.body);
  // console.log('The playlist contains these tracks: ', data.body.items[0].track);
  // console.log("'" + playlistName + "'" + ' contains these tracks:');
  let tracks = [];

  for (let track_obj of data.body.items) {
    const track = track_obj.track
    tracks.push(track);
    console.log(track.name + " : " + track.artists[0].name)
  }
  
  console.log("---------------+++++++++++++++++++++++++")
  return tracks;
}

getMyData();
