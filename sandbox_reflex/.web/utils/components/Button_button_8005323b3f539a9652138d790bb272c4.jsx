
import {Fragment,memo,useCallback,useContext,useEffect} from "react"
import {ReflexEvent,applyEventActions,isTrue} from "$/utils/state"
import {Button as RadixThemesButton} from "@radix-ui/themes"
import {EventLoopContext} from "$/utils/context"
import {jsx} from "@emotion/react"






export const Button_button_8005323b3f539a9652138d790bb272c4 = memo(({children}) => {
    const [addEvents, connectErrors] = useContext(EventLoopContext);
const on_click_3c6be42fe06f59e290eccea85cff7b90 = useCallback(((_e) => (addEvents([(ReflexEvent("reflex___state____state.sandbox_reflex___state_usuarios____usuario_state.save_usuario", ({  }), ({  })))], [_e], ({  })))), [addEvents, ReflexEvent])



    return(
        jsx(RadixThemesButton,{css:({ ["backgroundColor"] : "#800000", ["color"] : "white", ["cursor"] : "pointer", ["&:hover"] : ({ ["backgroundColor"] : "#A30000" }) }),onClick:on_click_3c6be42fe06f59e290eccea85cff7b90},children)
    )
});
